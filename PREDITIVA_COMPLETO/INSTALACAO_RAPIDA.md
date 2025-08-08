# 🚀 Instalação Rápida - PREDITIVA

## ⚡ Início em 5 Minutos

### 1. Extrair o Projeto
```bash
unzip PREDITIVA_COMPLETO.zip
cd PREDITIVA_COMPLETO
```

### 2. Instalar Dependências
```bash
pip install -r requirements.txt
```

### 3. Testar Instalação
```bash
cd scripts
python analyze_data.py
```

## 📁 Estrutura do Projeto

```
PREDITIVA_COMPLETO/
├── 📊 scripts/              # Scripts de análise
│   ├── analyze_data.py      # Análise financeira
│   ├── process_data.py      # Análise de processos
│   └── distribute_tasks.py  # Distribuição de tarefas
├── 👥 crm/                  # Sistema CRM
│   └── crm_module.py
├── ⚖️ nucleo_estrategico_pecas/  # Processamento de documentos
│   └── main.py
├── 📂 dados/                # Seus arquivos de dados
├── 📖 documentacao/         # Documentação completa
│   ├── README.md           # Documentação técnica
│   └── MANUAL_USUARIO.md   # Manual do usuário
├── ⚙️ config.json          # Configurações
└── 📋 requirements.txt     # Dependências Python
```

## 🎯 Primeiros Passos

### Análise Financeira
1. Coloque sua planilha `MOVIMENTAÇÃO FINANCEIRA (1).xlsx` na pasta `dados/`
2. Execute: `python scripts/analyze_data.py`
3. Veja o resultado em `analise_financeira.json`

### Análise de Processos
1. Coloque sua planilha `PROCESSOS 10.xlsx` na pasta `dados/`
2. Execute: `python scripts/process_data.py`
3. Veja alertas de prazo no terminal

### Sistema CRM
1. Execute: `python crm/crm_module.py`
2. Dados salvos em `crm_data.json`

## 🔧 Configuração

Edite o arquivo `config.json` para:
- Alterar nomes de arquivos
- Ativar/desativar módulos
- Ajustar configurações regionais

## 📞 Suporte

- **Manual Completo:** `documentacao/MANUAL_USUARIO.md`
- **Documentação Técnica:** `documentacao/README.md`

---

**PREDITIVA v1.0.0** - Sistema Integrado de Gestão Jurídica com IA

