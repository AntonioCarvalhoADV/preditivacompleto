#!/usr/bin/env python3
"""
PREDITIVA - Análise de Dados Financeiros
Script para análise de movimentação financeira do escritório
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import json
import os

class FinancialAnalyzer:
    def __init__(self, excel_file):
        """
        Inicializa o analisador financeiro
        
        Args:
            excel_file (str): Caminho para o arquivo Excel de movimentação financeira
        """
        self.excel_file = excel_file
        self.df = None
        self.analysis_results = {}
        
    def load_data(self):
        """Carrega os dados do arquivo Excel"""
        try:
            self.df = pd.read_excel(self.excel_file)
            print(f"✅ Dados carregados: {len(self.df)} registros")
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
        date_columns = ['Data', 'Data_Vencimento', 'Data_Pagamento']
        for col in date_columns:
            if col in self.df.columns:
                self.df[col] = pd.to_datetime(self.df[col], errors='coerce')
        
        # Converter valores monetários
        money_columns = ['Valor', 'Valor_Pago', 'Honorarios']
        for col in money_columns:
            if col in self.df.columns:
                self.df[col] = pd.to_numeric(self.df[col], errors='coerce')
        
        print("✅ Dados limpos e preparados")
        return True
    
    def analyze_revenue(self):
        """Analisa receitas e faturamento"""
        if 'Valor' not in self.df.columns:
            return
            
        # Receita total
        total_revenue = self.df['Valor'].sum()
        
        # Receita por mês
        if 'Data' in self.df.columns:
            monthly_revenue = self.df.groupby(self.df['Data'].dt.to_period('M'))['Valor'].sum()
        
        # Receita por tipo de serviço
        if 'Tipo_Servico' in self.df.columns:
            service_revenue = self.df.groupby('Tipo_Servico')['Valor'].sum()
        
        self.analysis_results['revenue'] = {
            'total': total_revenue,
            'monthly': monthly_revenue.to_dict() if 'Data' in self.df.columns else {},
            'by_service': service_revenue.to_dict() if 'Tipo_Servico' in self.df.columns else {}
        }
    
    def analyze_expenses(self):
        """Analisa despesas e custos"""
        # Filtrar despesas (valores negativos ou categoria específica)
        expenses = self.df[self.df['Valor'] < 0] if 'Valor' in self.df.columns else pd.DataFrame()
        
        if not expenses.empty:
            total_expenses = abs(expenses['Valor'].sum())
            
            # Despesas por categoria
            if 'Categoria' in expenses.columns:
                category_expenses = expenses.groupby('Categoria')['Valor'].sum().abs()
            
            self.analysis_results['expenses'] = {
                'total': total_expenses,
                'by_category': category_expenses.to_dict() if 'Categoria' in expenses.columns else {}
            }
    
    def analyze_clients(self):
        """Analisa dados de clientes"""
        if 'Cliente' not in self.df.columns:
            return
            
        # Top clientes por valor
        top_clients = self.df.groupby('Cliente')['Valor'].sum().sort_values(ascending=False).head(10)
        
        # Número de casos por cliente
        cases_per_client = self.df['Cliente'].value_counts().head(10)
        
        self.analysis_results['clients'] = {
            'top_by_value': top_clients.to_dict(),
            'top_by_cases': cases_per_client.to_dict()
        }
    
    def generate_insights(self):
        """Gera insights e recomendações"""
        insights = []
        
        if 'revenue' in self.analysis_results:
            total_revenue = self.analysis_results['revenue']['total']
            insights.append(f"💰 Receita total: R$ {total_revenue:,.2f}")
        
        if 'expenses' in self.analysis_results:
            total_expenses = self.analysis_results['expenses']['total']
            profit = total_revenue - total_expenses if 'revenue' in self.analysis_results else 0
            insights.append(f"💸 Despesas totais: R$ {total_expenses:,.2f}")
            insights.append(f"📈 Lucro líquido: R$ {profit:,.2f}")
        
        self.analysis_results['insights'] = insights
    
    def save_results(self, output_file='analise_financeira.json'):
        """Salva os resultados da análise"""
        # Converter objetos Period para string para serialização JSON
        results_copy = self.analysis_results.copy()
        if 'revenue' in results_copy and 'monthly' in results_copy['revenue']:
            monthly_str = {str(k): v for k, v in results_copy['revenue']['monthly'].items()}
            results_copy['revenue']['monthly'] = monthly_str
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(results_copy, f, indent=2, ensure_ascii=False, default=str)
        
        print(f"✅ Resultados salvos em: {output_file}")
    
    def run_analysis(self):
        """Executa análise completa"""
        print("🔍 Iniciando análise financeira...")
        
        if not self.load_data():
            return False
        
        if not self.clean_data():
            return False
        
        self.analyze_revenue()
        self.analyze_expenses()
        self.analyze_clients()
        self.generate_insights()
        
        print("✅ Análise concluída!")
        return True

def main():
    """Função principal"""
    # Verificar se arquivo existe
    excel_file = "MOVIMENTAÇÃO FINANCEIRA (1).xlsx"
    if not os.path.exists(excel_file):
        print(f"❌ Arquivo não encontrado: {excel_file}")
        print("📝 Coloque o arquivo Excel na mesma pasta do script")
        return
    
    # Executar análise
    analyzer = FinancialAnalyzer(excel_file)
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

