#!/usr/bin/env python3
"""
PREDITIVA - Módulo CRM (Customer Relationship Management)
Sistema de gestão de relacionamento com clientes
"""

import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional

class CRMModule:
    def __init__(self, data_file='crm_data.json'):
        """
        Inicializa o módulo CRM
        
        Args:
            data_file (str): Arquivo JSON para armazenar dados do CRM
        """
        self.data_file = data_file
        self.data = self.load_data()
    
    def load_data(self) -> Dict:
        """Carrega dados do arquivo JSON"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Erro ao carregar dados: {e}")
        
        # Estrutura inicial se arquivo não existe
        return {
            'clients': {},
            'interactions': [],
            'opportunities': [],
            'tasks': [],
            'settings': {
                'created_at': datetime.now().isoformat(),
                'version': '1.0'
            }
        }
    
    def save_data(self):
        """Salva dados no arquivo JSON"""
        try:
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, indent=2, ensure_ascii=False, default=str)
            return True
        except Exception as e:
            print(f"Erro ao salvar dados: {e}")
            return False
    
    def add_client(self, client_data: Dict) -> str:
        """
        Adiciona um novo cliente
        
        Args:
            client_data (Dict): Dados do cliente
            
        Returns:
            str: ID do cliente criado
        """
        client_id = f"CLI_{len(self.data['clients']) + 1:04d}"
        
        client = {
            'id': client_id,
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat(),
            'status': 'ativo',
            **client_data
        }
        
        self.data['clients'][client_id] = client
        self.save_data()
        
        print(f"✅ Cliente {client_id} adicionado com sucesso")
        return client_id
    
    def update_client(self, client_id: str, updates: Dict) -> bool:
        """
        Atualiza dados de um cliente
        
        Args:
            client_id (str): ID do cliente
            updates (Dict): Dados a serem atualizados
            
        Returns:
            bool: True se atualizado com sucesso
        """
        if client_id not in self.data['clients']:
            print(f"❌ Cliente {client_id} não encontrado")
            return False
        
        self.data['clients'][client_id].update(updates)
        self.data['clients'][client_id]['updated_at'] = datetime.now().isoformat()
        
        self.save_data()
        print(f"✅ Cliente {client_id} atualizado com sucesso")
        return True
    
    def get_client(self, client_id: str) -> Optional[Dict]:
        """
        Busca um cliente por ID
        
        Args:
            client_id (str): ID do cliente
            
        Returns:
            Dict: Dados do cliente ou None se não encontrado
        """
        return self.data['clients'].get(client_id)
    
    def search_clients(self, query: str) -> List[Dict]:
        """
        Busca clientes por nome, email ou telefone
        
        Args:
            query (str): Termo de busca
            
        Returns:
            List[Dict]: Lista de clientes encontrados
        """
        results = []
        query_lower = query.lower()
        
        for client in self.data['clients'].values():
            if (query_lower in client.get('nome', '').lower() or
                query_lower in client.get('email', '').lower() or
                query_lower in client.get('telefone', '').lower()):
                results.append(client)
        
        return results
    
    def add_interaction(self, client_id: str, interaction_data: Dict) -> str:
        """
        Adiciona uma interação com cliente
        
        Args:
            client_id (str): ID do cliente
            interaction_data (Dict): Dados da interação
            
        Returns:
            str: ID da interação criada
        """
        interaction_id = f"INT_{len(self.data['interactions']) + 1:04d}"
        
        interaction = {
            'id': interaction_id,
            'client_id': client_id,
            'created_at': datetime.now().isoformat(),
            **interaction_data
        }
        
        self.data['interactions'].append(interaction)
        self.save_data()
        
        print(f"✅ Interação {interaction_id} registrada")
        return interaction_id
    
    def get_client_interactions(self, client_id: str) -> List[Dict]:
        """
        Busca todas as interações de um cliente
        
        Args:
            client_id (str): ID do cliente
            
        Returns:
            List[Dict]: Lista de interações do cliente
        """
        return [
            interaction for interaction in self.data['interactions']
            if interaction['client_id'] == client_id
        ]
    
    def add_opportunity(self, opportunity_data: Dict) -> str:
        """
        Adiciona uma oportunidade de negócio
        
        Args:
            opportunity_data (Dict): Dados da oportunidade
            
        Returns:
            str: ID da oportunidade criada
        """
        opportunity_id = f"OPP_{len(self.data['opportunities']) + 1:04d}"
        
        opportunity = {
            'id': opportunity_id,
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat(),
            'status': 'aberta',
            **opportunity_data
        }
        
        self.data['opportunities'].append(opportunity)
        self.save_data()
        
        print(f"✅ Oportunidade {opportunity_id} criada")
        return opportunity_id
    
    def add_task(self, task_data: Dict) -> str:
        """
        Adiciona uma tarefa
        
        Args:
            task_data (Dict): Dados da tarefa
            
        Returns:
            str: ID da tarefa criada
        """
        task_id = f"TSK_{len(self.data['tasks']) + 1:04d}"
        
        task = {
            'id': task_id,
            'created_at': datetime.now().isoformat(),
            'status': 'pendente',
            **task_data
        }
        
        self.data['tasks'].append(task)
        self.save_data()
        
        print(f"✅ Tarefa {task_id} criada")
        return task_id
    
    def get_pending_tasks(self) -> List[Dict]:
        """
        Busca tarefas pendentes
        
        Returns:
            List[Dict]: Lista de tarefas pendentes
        """
        return [
            task for task in self.data['tasks']
            if task['status'] == 'pendente'
        ]
    
    def get_overdue_tasks(self) -> List[Dict]:
        """
        Busca tarefas em atraso
        
        Returns:
            List[Dict]: Lista de tarefas em atraso
        """
        today = datetime.now().date()
        overdue = []
        
        for task in self.data['tasks']:
            if (task['status'] == 'pendente' and 
                'due_date' in task and 
                datetime.fromisoformat(task['due_date']).date() < today):
                overdue.append(task)
        
        return overdue
    
    def generate_report(self) -> Dict:
        """
        Gera relatório do CRM
        
        Returns:
            Dict: Relatório com estatísticas
        """
        total_clients = len(self.data['clients'])
        active_clients = len([c for c in self.data['clients'].values() if c['status'] == 'ativo'])
        total_interactions = len(self.data['interactions'])
        open_opportunities = len([o for o in self.data['opportunities'] if o['status'] == 'aberta'])
        pending_tasks = len(self.get_pending_tasks())
        overdue_tasks = len(self.get_overdue_tasks())
        
        return {
            'clients': {
                'total': total_clients,
                'active': active_clients
            },
            'interactions': {
                'total': total_interactions
            },
            'opportunities': {
                'open': open_opportunities
            },
            'tasks': {
                'pending': pending_tasks,
                'overdue': overdue_tasks
            },
            'generated_at': datetime.now().isoformat()
        }

def main():
    """Função principal para demonstração"""
    crm = CRMModule()
    
    print("🏢 PREDITIVA - Módulo CRM")
    print("=" * 40)
    
    # Exemplo de uso
    client_id = crm.add_client({
        'nome': 'João Silva',
        'email': 'joao@email.com',
        'telefone': '(11) 99999-9999',
        'empresa': 'Silva & Associados',
        'area_interesse': 'Direito Empresarial'
    })
    
    # Adicionar interação
    crm.add_interaction(client_id, {
        'tipo': 'ligacao',
        'descricao': 'Primeira consulta sobre constituição de empresa',
        'duracao': 30
    })
    
    # Adicionar oportunidade
    crm.add_opportunity({
        'client_id': client_id,
        'titulo': 'Constituição de Empresa',
        'valor_estimado': 5000.00,
        'probabilidade': 80
    })
    
    # Gerar relatório
    report = crm.generate_report()
    print("\n📊 RELATÓRIO CRM:")
    print(f"Clientes ativos: {report['clients']['active']}")
    print(f"Interações registradas: {report['interactions']['total']}")
    print(f"Oportunidades abertas: {report['opportunities']['open']}")
    print(f"Tarefas pendentes: {report['tasks']['pending']}")

if __name__ == "__main__":
    main()

