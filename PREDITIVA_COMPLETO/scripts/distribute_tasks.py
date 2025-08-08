#!/usr/bin/env python3
"""
PREDITIVA - Distribuição de Tarefas
Script para distribuir tarefas entre membros da equipe
"""

import json
import pandas as pd
from datetime import datetime
import random

class TaskDistributor:
    def __init__(self, team_file='team_data.csv', tasks_file='tasks_input.json'):
        """
        Inicializa o distribuidor de tarefas
        
        Args:
            team_file (str): Arquivo CSV com dados da equipe
            tasks_file (str): Arquivo JSON com tarefas a distribuir
        """
        self.team_file = team_file
        self.tasks_file = tasks_file
        self.team_data = None
        self.tasks_data = None
        self.distribution = {}
    
    def load_team_data(self):
        """Carrega dados da equipe"""
        try:
            self.team_data = pd.read_csv(self.team_file)
            print(f"✅ Equipe carregada: {len(self.team_data)} membros")
            return True
        except Exception as e:
            print(f"❌ Erro ao carregar equipe: {e}")
            return False
    
    def load_tasks_data(self):
        """Carrega dados das tarefas"""
        try:
            with open(self.tasks_file, 'r', encoding='utf-8') as f:
                self.tasks_data = json.load(f)
            print(f"✅ Tarefas carregadas: {len(self.tasks_data)} tarefas")
            return True
        except Exception as e:
            print(f"❌ Erro ao carregar tarefas: {e}")
            return False
    
    def match_skills(self, task_skill, member_skills):
        """
        Verifica compatibilidade entre habilidade da tarefa e do membro
        
        Args:
            task_skill (str): Habilidade requerida pela tarefa
            member_skills (str): Habilidades do membro (separadas por vírgula)
            
        Returns:
            int: Pontuação de compatibilidade (0-100)
        """
        if not task_skill or not member_skills:
            return 50  # Pontuação neutra
        
        task_skill_lower = task_skill.lower()
        member_skills_lower = member_skills.lower()
        
        # Correspondência exata
        if task_skill_lower in member_skills_lower:
            return 100
        
        # Correspondências parciais
        skill_keywords = {
            'petição': ['redação', 'escrita', 'jurídica'],
            'pesquisa': ['análise', 'investigação', 'jurisprudência'],
            'audiência': ['oratória', 'comunicação', 'representação'],
            'organização': ['arquivo', 'documentos', 'gestão'],
            'comunicação': ['atendimento', 'relacionamento', 'cliente']
        }
        
        for keyword, related in skill_keywords.items():
            if keyword in task_skill_lower:
                for rel in related:
                    if rel in member_skills_lower:
                        return 75
        
        return 25  # Pontuação baixa se não há correspondência
    
    def calculate_workload(self, member_name):
        """
        Calcula carga de trabalho atual do membro
        
        Args:
            member_name (str): Nome do membro
            
        Returns:
            int: Número de tarefas já atribuídas
        """
        return len([task for task in self.distribution.values() 
                   if task.get('responsavel') == member_name])
    
    def distribute_tasks(self):
        """Distribui tarefas entre membros da equipe"""
        if self.team_data is None or self.tasks_data is None:
            print("❌ Dados não carregados")
            return False
        
        print("🔄 Iniciando distribuição de tarefas...")
        
        for i, task in enumerate(self.tasks_data):
            task_id = f"TASK_{i+1:03d}"
            best_member = None
            best_score = -1
            
            # Avaliar cada membro da equipe
            for _, member in self.team_data.iterrows():
                # Calcular pontuação baseada em habilidades
                skill_score = self.match_skills(
                    task.get('habilidade', ''),
                    member.get('Habilidades', '')
                )
                
                # Penalizar por carga de trabalho alta
                workload = self.calculate_workload(member['Nome'])
                workload_penalty = workload * 10  # 10 pontos por tarefa já atribuída
                
                # Pontuação final
                final_score = skill_score - workload_penalty
                
                if final_score > best_score:
                    best_score = final_score
                    best_member = member['Nome']
            
            # Atribuir tarefa ao melhor membro
            self.distribution[task_id] = {
                'tarefa': task.get('descricao', 'Tarefa sem descrição'),
                'responsavel': best_member,
                'habilidade_requerida': task.get('habilidade', ''),
                'prioridade': task.get('prioridade', 'Média'),
                'pontuacao_compatibilidade': best_score,
                'data_atribuicao': datetime.now().isoformat()
            }
        
        print("✅ Distribuição concluída!")
        return True
    
    def save_distribution(self, output_file='tarefas_semana.json'):
        """Salva a distribuição de tarefas"""
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(self.distribution, f, indent=2, ensure_ascii=False, default=str)
            print(f"✅ Distribuição salva em: {output_file}")
            return True
        except Exception as e:
            print(f"❌ Erro ao salvar: {e}")
            return False
    
    def generate_summary(self):
        """Gera resumo da distribuição"""
        if not self.distribution:
            return
        
        print("\n📋 RESUMO DA DISTRIBUIÇÃO:")
        print("=" * 50)
        
        # Contar tarefas por pessoa
        person_counts = {}
        for task in self.distribution.values():
            person = task['responsavel']
            person_counts[person] = person_counts.get(person, 0) + 1
        
        for person, count in person_counts.items():
            print(f"👤 {person}: {count} tarefas")
        
        # Tarefas por prioridade
        priority_counts = {}
        for task in self.distribution.values():
            priority = task['prioridade']
            priority_counts[priority] = priority_counts.get(priority, 0) + 1
        
        print("\n📊 Por prioridade:")
        for priority, count in priority_counts.items():
            print(f"🔥 {priority}: {count} tarefas")

def main():
    """Função principal"""
    distributor = TaskDistributor()
    
    # Verificar se arquivos existem
    import os
    if not os.path.exists(distributor.team_file):
        print(f"❌ Arquivo da equipe não encontrado: {distributor.team_file}")
        return
    
    if not os.path.exists(distributor.tasks_file):
        print(f"❌ Arquivo de tarefas não encontrado: {distributor.tasks_file}")
        return
    
    # Executar distribuição
    if distributor.load_team_data() and distributor.load_tasks_data():
        if distributor.distribute_tasks():
            distributor.save_distribution()
            distributor.generate_summary()

if __name__ == "__main__":
    main()

