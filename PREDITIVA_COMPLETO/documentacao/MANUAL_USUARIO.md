# Manual do Usuário - PREDITIVA

## 🎯 Guia Rápido de Início

### Primeiros Passos

1. **Extrair o projeto**
2. **Instalar dependências** (`pip install -r requirements.txt`)
3. **Preparar seus dados** (planilhas Excel)
4. **Executar análises**

### Estrutura de Pastas

```
PREDITIVA_COMPLETO/
├── scripts/           # Scripts principais de análise
├── crm/              # Sistema de CRM
├── nucleo_estrategico_pecas/  # Processamento de documentos
├── dados/            # Seus arquivos de dados
├── documentacao/     # Documentação completa
└── config.json       # Configurações do sistema
```

## 📊 Módulo: Análise Financeira

### O que faz
Analisa sua movimentação financeira e gera insights sobre receitas, despesas e lucratividade.

### Como usar

1. **Prepare sua planilha:**
   - Nome do arquivo: `MOVIMENTAÇÃO FINANCEIRA (1).xlsx`
   - Colunas necessárias: Data, Valor, Cliente, Tipo_Servico, Categoria

2. **Execute o script:**
   ```bash
   cd scripts
   python analyze_data.py
   ```

3. **Verifique os resultados:**
   - Arquivo gerado: `analise_financeira.json`
   - Insights exibidos no terminal

### Interpretando os Resultados

- **Receita Total:** Soma de todas as receitas do período
- **Despesas Totais:** Soma de todas as despesas
- **Lucro Líquido:** Receita - Despesas
- **Top Clientes:** Clientes que mais geram receita
- **Receita Mensal:** Evolução mês a mês

## 📁 Módulo: Análise de Processos

### O que faz
Monitora seus processos jurídicos, identifica prazos vencidos e analisa performance por área.

### Como usar

1. **Prepare sua planilha:**
   - Nome do arquivo: `PROCESSOS 10.xlsx`
   - Colunas necessárias: Numero_Processo, Cliente, Status, Prazo, Area_Juridica, Responsavel

2. **Execute o script:**
   ```bash
   cd scripts
   python process_data.py
   ```

3. **Verifique os resultados:**
   - Arquivo gerado: `analise_processos.json`
   - Alertas de prazo exibidos no terminal

### Alertas Importantes

- 🚨 **Processos com prazo vencido:** Ação imediata necessária
- ⏰ **Prazos próximos (7 dias):** Prepare-se com antecedência
- 📈 **Performance por área:** Identifique gargalos

## 👥 Módulo: CRM

### O que faz
Gerencia seus clientes, interações, oportunidades e tarefas de relacionamento.

### Como usar

1. **Inicie o sistema:**
   ```bash
   cd crm
   python crm_module.py
   ```

2. **Funcionalidades principais:**
   - Adicionar novos clientes
   - Registrar interações
   - Criar oportunidades de negócio
   - Gerenciar tarefas

### Exemplo de Uso

```python
# Adicionar cliente
client_id = crm.add_client({
    'nome': 'João Silva',
    'email': 'joao@email.com',
    'telefone': '(11) 99999-9999',
    'empresa': 'Silva & Associados'
})

# Registrar interação
crm.add_interaction(client_id, {
    'tipo': 'ligacao',
    'descricao': 'Consulta sobre direito empresarial',
    'duracao': 30
})
```

## 📋 Módulo: Distribuição de Tarefas

### O que faz
Distribui tarefas entre sua equipe baseado em habilidades e carga de trabalho atual.

### Como usar

1. **Prepare os arquivos:**
   
   **team_data.csv:**
   ```csv
   Nome,Função,Habilidades
   João Silva,Advogado Senior,Petição,Audiência,Pesquisa Jurídica
   Maria Santos,Advogada Junior,Pesquisa,Organização,Comunicação
   ```
   
   **tasks_input.json:**
   ```json
   [
     {
       "descricao": "Elaborar petição inicial",
       "habilidade": "Petição",
       "prioridade": "Alta"
     },
     {
       "descricao": "Pesquisar jurisprudência",
       "habilidade": "Pesquisa",
       "prioridade": "Média"
     }
   ]
   ```

2. **Execute o script:**
   ```bash
   cd scripts
   python distribute_tasks.py
   ```

3. **Resultado:**
   - Arquivo: `tarefas_semana.json`
   - Resumo da distribuição no terminal

## ⚖️ Módulo: Núcleo Estratégico de Peças

### O que faz
Processa documentos jurídicos (PDF, DOCX, TXT) e extrai informações relevantes.

### Como usar

1. **Inicie o sistema:**
   ```bash
   cd nucleo_estrategico_pecas
   python main.py
   ```

2. **Processe documentos:**
   ```python
   # Exemplo de processamento
   nucleo = NucleoEstrategicoPecas()
   resultado = nucleo.process_document('documento.pdf', 'processo')
   ```

3. **Resultados:**
   - Pasta: `pecas_processadas/`
   - Análise de cada documento em JSON
   - Relatório resumo: `relatorio_nucleo_pecas.json`

### Informações Extraídas

- **Áreas jurídicas** identificadas no documento
- **Termos-chave** jurídicos encontrados
- **Indicadores de urgência**
- **Número de processo** (se presente)
- **Partes envolvidas**

## ⚙️ Configurações Avançadas

### Arquivo config.json

Personalize o comportamento do sistema:

```json
{
  "modulos": {
    "analise_financeira": {
      "ativo": true,
      "arquivo_entrada": "SEU_ARQUIVO_FINANCEIRO.xlsx"
    }
  },
  "configuracoes": {
    "timezone": "America/Sao_Paulo",
    "formato_data": "%d/%m/%Y"
  }
}
```

### Personalizações Comuns

- **Nomes de arquivos:** Ajuste para seus arquivos específicos
- **Colunas das planilhas:** Adapte aos seus formatos
- **Timezone:** Configure para sua região
- **Formatos de data:** Ajuste conforme necessário

## 🔧 Solução de Problemas

### Problemas Comuns

**Erro: "Arquivo não encontrado"**
- Verifique se o arquivo está na pasta correta
- Confirme o nome exato do arquivo
- Verifique as permissões de leitura

**Erro: "Módulo não encontrado"**
- Execute: `pip install -r requirements.txt`
- Verifique se está no ambiente Python correto

**Dados não aparecem corretamente**
- Verifique os nomes das colunas na planilha
- Confirme o formato dos dados (datas, números)
- Verifique o encoding do arquivo (UTF-8)

### Logs e Depuração

- Mensagens de erro aparecem no terminal
- Arquivos de log são salvos junto com os resultados
- Use `print()` para depuração adicional

## 📈 Interpretando Relatórios

### Relatório Financeiro

```json
{
  "revenue": {
    "total": 150000.00,
    "monthly": {"2025-06": 25000.00},
    "by_service": {"Consultoria": 80000.00}
  },
  "insights": [
    "💰 Receita total: R$ 150,000.00",
    "📈 Lucro líquido: R$ 120,000.00"
  ]
}
```

### Relatório de Processos

```json
{
  "deadlines": {
    "overdue_count": 3,
    "upcoming_count": 5,
    "overdue_processes": [...]
  },
  "insights": [
    "🚨 ATENÇÃO: 3 processos com prazo vencido!",
    "⏰ 5 processos com prazo próximo (7 dias)"
  ]
}
```

## 🎯 Dicas de Uso

### Melhores Práticas

1. **Execute análises regularmente** (semanal/mensal)
2. **Mantenha dados atualizados** nas planilhas
3. **Faça backup** dos arquivos de configuração
4. **Monitore alertas** de prazo constantemente
5. **Use o CRM** para todas as interações com clientes

### Otimização

- **Automatize** execuções com scripts de agendamento
- **Integre** com suas ferramentas existentes
- **Customize** relatórios para suas necessidades
- **Treine** sua equipe no uso dos módulos

## 📞 Suporte

### Recursos de Ajuda

- **Documentação completa:** `documentacao/README.md`
- **Exemplos práticos:** Pasta `dados/`
- **Configurações:** `config.json`

### Contato

Para suporte técnico ou dúvidas específicas, consulte a documentação técnica ou entre em contato com a equipe de desenvolvimento.

---

*Este manual foi criado para facilitar o uso do PREDITIVA. Para informações técnicas detalhadas, consulte a documentação completa.*

