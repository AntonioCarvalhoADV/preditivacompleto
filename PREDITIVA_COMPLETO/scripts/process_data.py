#!/usr/bin/env python3
"""
PREDITIVA - Análise de Processos Jurídicos
Script para análise de dados de processos do escritório
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import json
import os

class ProcessAnalyzer:
    def __init__(self, excel_file):
        """
        Inicializa o analisador de processos
        
        Args:
            excel_file (str): Caminho para o arquivo Excel de processos
        """
        self.excel_file = excel_file
        self.df = None
        self.analysis_results = {}
        
    def load_data(self):
        """Carrega os dados do arquivo Excel"""
        try:
            self.df = pd.read_excel(self.excel_file)
            print(f"✅ Dados carregados: {len(self.df)} processos")
            return True
        except Exception as e:
            print(f"❌ Erro ao carregar dados: {e}")
            return False
    
    def clean_data(self):
        """Limpa e prepara os dados para análise"""
        if self.df is None:
            print("❌ Dados não carregados")
            return False
            
        # Converter colunas de data
        date_columns = ['Data_Inicio', 'Data_Audiencia', 'Prazo', 'Ultima_Movimentacao']
        for col in date_columns:
            if col in self.df.columns:
                self.df[col] = pd.to_datetime(self.df[col], errors='coerce')
        
        # Converter valores monetários
        money_columns = ['Valor_Causa', 'Honorarios', 'Custas']
        for col in money_columns:
            if col in self.df.columns:
                self.df[col] = pd.to_numeric(self.df[col], errors='coerce')
        
        print("✅ Dados limpos e preparados")
        return True
    
    def analyze_status(self):
        """Analisa status dos processos"""
        if 'Status' not in self.df.columns:
            return
            
        status_counts = self.df['Status'].value_counts()
        status_percentages = self.df['Status'].value_counts(normalize=True) * 100
        
        self.analysis_results['status'] = {
            'counts': status_counts.to_dict(),
            'percentages': status_percentages.to_dict()
        }
    
    def analyze_areas(self):
        """Analisa áreas jurídicas"""
        if 'Area_Juridica' not in self.df.columns:
            return
            
        area_counts = self.df['Area_Juridica'].value_counts()
        
        # Valor médio por área
        if 'Valor_Causa' in self.df.columns:
            avg_value_by_area = self.df.groupby('Area_Juridica')['Valor_Causa'].mean()
        
        self.analysis_results['areas'] = {
            'counts': area_counts.to_dict(),
            'avg_values': avg_value_by_area.to_dict() if 'Valor_Causa' in self.df.columns else {}
        }
    
    def analyze_deadlines(self):
        """Analisa prazos e urgências"""
        if 'Prazo' not in self.df.columns:
            return
            
        today = datetime.now()
        
        # Processos com prazo vencido
        overdue = self.df[self.df['Prazo'] < today]
        
        # Processos com prazo próximo (próximos 7 dias)
        upcoming = self.df[
            (self.df['Prazo'] >= today) & 
            (self.df['Prazo'] <= today + timedelta(days=7))
        ]
        
        self.analysis_results['deadlines'] = {
            'overdue_count': len(overdue),
            'upcoming_count': len(upcoming),
            'overdue_processes': overdue[['Numero_Processo', 'Cliente', 'Prazo']].to_dict('records') if not overdue.empty else [],
            'upcoming_processes': upcoming[['Numero_Processo', 'Cliente', 'Prazo']].to_dict('records') if not upcoming.empty else []
        }
    
    def analyze_team_performance(self):
        """Analisa performance da equipe"""
        if 'Responsavel' not in self.df.columns:
            return
            
        # Processos por responsável
        processes_per_person = self.df['Responsavel'].value_counts()
        
        # Taxa de sucesso por responsável (se houver coluna de resultado)
        if 'Resultado' in self.df.columns:
            success_rate = self.df.groupby('Responsavel')['Resultado'].apply(
                lambda x: (x == 'Favorável').mean() * 100
            )
        
        self.analysis_results['team'] = {
            'processes_per_person': processes_per_person.to_dict(),
            'success_rates': success_rate.to_dict() if 'Resultado' in self.df.columns else {}
        }
    
    def analyze_clients(self):
        """Analisa dados de clientes"""
        if 'Cliente' not in self.df.columns:
            return
            
        # Processos por cliente
        processes_per_client = self.df['Cliente'].value_counts().head(10)
        
        # Valor total por cliente
        if 'Valor_Causa' in self.df.columns:
            value_per_client = self.df.groupby('Cliente')['Valor_Causa'].sum().sort_values(ascending=False).head(10)
        
        self.analysis_results['clients'] = {
            'top_by_processes': processes_per_client.to_dict(),
            'top_by_value': value_per_client.to_dict() if 'Valor_Causa' in self.df.columns else {}
        }
    
    def generate_insights(self):
        """Gera insights e recomendações"""
        insights = []
        
        # Total de processos
        total_processes = len(self.df)
        insights.append(f"📁 Total de processos: {total_processes}")
        
        # Processos ativos
        if 'status' in self.analysis_results:
            active_processes = sum([
                count for status, count in self.analysis_results['status']['counts'].items()
                if status.lower() not in ['arquivado', 'finalizado', 'encerrado']
            ])
            insights.append(f"⚡ Processos ativos: {active_processes}")
        
        # Alertas de prazo
        if 'deadlines' in self.analysis_results:
            overdue = self.analysis_results['deadlines']['overdue_count']
            upcoming = self.analysis_results['deadlines']['upcoming_count']
            
            if overdue > 0:
                insights.append(f"🚨 ATENÇÃO: {overdue} processos com prazo vencido!")
            if upcoming > 0:
                insights.append(f"⏰ {upcoming} processos com prazo próximo (7 dias)")
        
        # Área mais movimentada
        if 'areas' in self.analysis_results:
            top_area = max(self.analysis_results['areas']['counts'].items(), key=lambda x: x[1])
            insights.append(f"🏛️ Área mais movimentada: {top_area[0]} ({top_area[1]} processos)")
        
        self.analysis_results['insights'] = insights
    
    def save_results(self, output_file='analise_processos.json'):
        """Salva os resultados da análise"""
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(self.analysis_results, f, indent=2, ensure_ascii=False, default=str)
        
        print(f"✅ Resultados salvos em: {output_file}")
    
    def run_analysis(self):
        """Executa análise completa"""
        print("🔍 Iniciando análise de processos...")
        
        if not self.load_data():
            return False
        
        if not self.clean_data():
            return False
        
        self.analyze_status()
        self.analyze_areas()
        self.analyze_deadlines()
        self.analyze_team_performance()
        self.analyze_clients()
        self.generate_insights()
        
        print("✅ Análise concluída!")
        return True

def main():
    """Função principal"""
    # Verificar se arquivo existe
    excel_file = "PROCESSOS 10.xlsx"
    if not os.path.exists(excel_file):
        print(f"❌ Arquivo não encontrado: {excel_file}")
        print("📝 Coloque o arquivo Excel na mesma pasta do script")
        return
    
    # Executar análise
    analyzer = ProcessAnalyzer(excel_file)
    if analyzer.run_analysis():
        analyzer.save_results()
        
        # Exibir insights
        if 'insights' in analyzer.analysis_results:
            print("\n📊 INSIGHTS PRINCIPAIS:")
            print("=" * 50)
            for insight in analyzer.analysis_results['insights']:
                print(insight)

if __name__ == "__main__":
    main()

