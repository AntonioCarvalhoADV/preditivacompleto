#!/usr/bin/env python3
"""
PREDITIVA - Núcleo Estratégico de Peças
Sistema para auxiliar na criação de peças processuais
"""

import os
import json
from datetime import datetime
from pathlib import Path
import PyPDF2
import docx
import re

class NucleoEstrategicoPecas:
    def __init__(self, output_dir='pecas_processadas'):
        """
        Inicializa o Núcleo Estratégico de Peças
        
        Args:
            output_dir (str): Diretório para salvar peças processadas
        """
        self.output_dir = output_dir
        self.create_output_dir()
        self.processed_documents = []
    
    def create_output_dir(self):
        """Cria diretório de saída se não existir"""
        Path(self.output_dir).mkdir(exist_ok=True)
    
    def extract_text_from_pdf(self, pdf_path):
        """
        Extrai texto de arquivo PDF
        
        Args:
            pdf_path (str): Caminho para o arquivo PDF
            
        Returns:
            str: Texto extraído
        """
        try:
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                text = ""
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
                return text
        except Exception as e:
            print(f"Erro ao extrair texto do PDF: {e}")
            return ""
    
    def extract_text_from_docx(self, docx_path):
        """
        Extrai texto de arquivo DOCX
        
        Args:
            docx_path (str): Caminho para o arquivo DOCX
            
        Returns:
            str: Texto extraído
        """
        try:
            doc = docx.Document(docx_path)
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            return text
        except Exception as e:
            print(f"Erro ao extrair texto do DOCX: {e}")
            return ""
    
    def extract_text_from_txt(self, txt_path):
        """
        Extrai texto de arquivo TXT
        
        Args:
            txt_path (str): Caminho para o arquivo TXT
            
        Returns:
            str: Texto extraído
        """
        try:
            with open(txt_path, 'r', encoding='utf-8') as file:
                return file.read()
        except Exception as e:
            print(f"Erro ao extrair texto do TXT: {e}")
            return ""
    
    def process_document(self, file_path, document_type="processo"):
        """
        Processa um documento e extrai informações relevantes
        
        Args:
            file_path (str): Caminho para o arquivo
            document_type (str): Tipo do documento
            
        Returns:
            dict: Informações extraídas do documento
        """
        file_extension = Path(file_path).suffix.lower()
        
        # Extrair texto baseado na extensão
        if file_extension == '.pdf':
            text = self.extract_text_from_pdf(file_path)
        elif file_extension == '.docx':
            text = self.extract_text_from_docx(file_path)
        elif file_extension == '.txt':
            text = self.extract_text_from_txt(file_path)
        else:
            print(f"Formato não suportado: {file_extension}")
            return None
        
        # Análise básica do texto
        analysis = self.analyze_document_content(text)
        
        # Criar registro do documento processado
        document_info = {
            'id': f"DOC_{len(self.processed_documents) + 1:04d}",
            'file_path': file_path,
            'file_name': Path(file_path).name,
            'document_type': document_type,
            'processed_at': datetime.now().isoformat(),
            'text_length': len(text),
            'analysis': analysis,
            'raw_text': text[:1000] + "..." if len(text) > 1000 else text  # Primeiros 1000 chars
        }
        
        self.processed_documents.append(document_info)
        
        # Salvar documento processado
        self.save_processed_document(document_info)
        
        return document_info
    
    def analyze_document_content(self, text):
        """
        Analisa o conteúdo do documento e extrai informações jurídicas
        
        Args:
            text (str): Texto do documento
            
        Returns:
            dict: Análise do conteúdo
        """
        analysis = {
            'word_count': len(text.split()),
            'has_process_number': bool(re.search(r'\d{7}-\d{2}\.\d{4}\.\d\.\d{2}\.\d{4}', text)),
            'mentions_court': bool(re.search(r'(tribunal|juiz|vara|comarca)', text, re.IGNORECASE)),
            'mentions_parties': bool(re.search(r'(autor|réu|requerente|requerido)', text, re.IGNORECASE)),
            'legal_areas': self.identify_legal_areas(text),
            'key_terms': self.extract_key_terms(text),
            'urgency_indicators': self.check_urgency(text)
        }
        
        return analysis
    
    def identify_legal_areas(self, text):
        """
        Identifica áreas jurídicas mencionadas no texto
        
        Args:
            text (str): Texto do documento
            
        Returns:
            list: Áreas jurídicas identificadas
        """
        areas = {
            'civil': ['civil', 'contrato', 'responsabilidade civil', 'danos morais'],
            'trabalhista': ['trabalhista', 'CLT', 'rescisão', 'FGTS', 'horas extras'],
            'criminal': ['criminal', 'penal', 'crime', 'delito', 'contravenção'],
            'tributario': ['tributário', 'imposto', 'ICMS', 'IPI', 'ISS', 'IR'],
            'previdenciario': ['previdenciário', 'INSS', 'aposentadoria', 'auxílio'],
            'empresarial': ['empresarial', 'societário', 'empresa', 'sócio']
        }
        
        identified_areas = []
        text_lower = text.lower()
        
        for area, keywords in areas.items():
            if any(keyword in text_lower for keyword in keywords):
                identified_areas.append(area)
        
        return identified_areas
    
    def extract_key_terms(self, text):
        """
        Extrai termos-chave do documento
        
        Args:
            text (str): Texto do documento
            
        Returns:
            list: Lista de termos-chave
        """
        # Termos jurídicos comuns
        legal_terms = [
            'petição inicial', 'contestação', 'tréplica', 'sentença', 'acórdão',
            'recurso', 'apelação', 'agravo', 'embargos', 'mandado de segurança',
            'liminar', 'tutela antecipada', 'medida cautelar', 'execução'
        ]
        
        found_terms = []
        text_lower = text.lower()
        
        for term in legal_terms:
            if term in text_lower:
                found_terms.append(term)
        
        return found_terms
    
    def check_urgency(self, text):
        """
        Verifica indicadores de urgência no documento
        
        Args:
            text (str): Texto do documento
            
        Returns:
            dict: Indicadores de urgência
        """
        urgency_keywords = ['urgente', 'prazo', 'liminar', 'antecipação', 'cautelar']
        text_lower = text.lower()
        
        urgency_score = sum(1 for keyword in urgency_keywords if keyword in text_lower)
        
        return {
            'score': urgency_score,
            'level': 'alta' if urgency_score >= 3 else 'média' if urgency_score >= 1 else 'baixa',
            'keywords_found': [kw for kw in urgency_keywords if kw in text_lower]
        }
    
    def save_processed_document(self, document_info):
        """
        Salva informações do documento processado
        
        Args:
            document_info (dict): Informações do documento
        """
        output_file = os.path.join(self.output_dir, f"{document_info['id']}_analysis.json")
        
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(document_info, f, indent=2, ensure_ascii=False, default=str)
            print(f"✅ Análise salva: {output_file}")
        except Exception as e:
            print(f"❌ Erro ao salvar análise: {e}")
    
    def generate_summary_report(self):
        """
        Gera relatório resumo dos documentos processados
        
        Returns:
            dict: Relatório resumo
        """
        if not self.processed_documents:
            return {'message': 'Nenhum documento processado'}
        
        total_docs = len(self.processed_documents)
        total_words = sum(doc['analysis']['word_count'] for doc in self.processed_documents)
        
        # Áreas jurídicas mais comuns
        all_areas = []
        for doc in self.processed_documents:
            all_areas.extend(doc['analysis']['legal_areas'])
        
        area_counts = {}
        for area in all_areas:
            area_counts[area] = area_counts.get(area, 0) + 1
        
        # Documentos urgentes
        urgent_docs = [
            doc for doc in self.processed_documents 
            if doc['analysis']['urgency_indicators']['level'] == 'alta'
        ]
        
        report = {
            'total_documents': total_docs,
            'total_words': total_words,
            'average_words_per_doc': total_words // total_docs if total_docs > 0 else 0,
            'legal_areas_frequency': area_counts,
            'urgent_documents': len(urgent_docs),
            'urgent_document_ids': [doc['id'] for doc in urgent_docs],
            'generated_at': datetime.now().isoformat()
        }
        
        return report
    
    def save_summary_report(self, output_file='relatorio_nucleo_pecas.json'):
        """
        Salva relatório resumo
        
        Args:
            output_file (str): Nome do arquivo de saída
        """
        report = self.generate_summary_report()
        
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(report, f, indent=2, ensure_ascii=False, default=str)
            print(f"✅ Relatório salvo: {output_file}")
        except Exception as e:
            print(f"❌ Erro ao salvar relatório: {e}")

def main():
    """Função principal para demonstração"""
    nucleo = NucleoEstrategicoPecas()
    
    print("⚖️ PREDITIVA - Núcleo Estratégico de Peças")
    print("=" * 50)
    
    # Exemplo de uso
    print("📁 Sistema pronto para processar documentos")
    print("Formatos suportados: PDF, DOCX, TXT")
    print(f"Diretório de saída: {nucleo.output_dir}")
    
    # Gerar relatório (mesmo que vazio inicialmente)
    nucleo.save_summary_report()

if __name__ == "__main__":
    main()

