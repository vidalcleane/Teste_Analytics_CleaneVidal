# Teste Analytics — Quod
Candidato: Maria Cleane Vidal Furtado

Repositório com a solução completa do Teste para Estagiário de Analytics da Quod.

## Estrutura do Repositório

```
Teste_Analytics_CleaneVidal/
│
├── 1_simulacao_limpeza.py       # Parte 1 – Tarefa 1: simulação e limpeza
├── 2_analise_exploratoria.py    # Parte 1 – Tarefa 2: EDA e visualizações
├── consultas_sql.sql            # Parte 2 – Consultas SQL
├── relatorio_insights.md        # Parte 3 – Relatório de insights
│
├── data_clean.csv               # Dataset limpo gerado pelo script 1
├── graficos_vendas.png          # Dashboard de visualizações gerado pelo script 2
│
└── README.md
```

## Contexto do Dataset

Os dados simulam vendas dos produtos reais da Quod ao longo de 2023:

| Produto | Categoria |
|---|---|
| Quod Score PF | Análise de Crédito |
| Quod Score PJ | Análise de Crédito |
| Quod X Antifraude | Prevenção a Fraude |
| Quod Identity | Prevenção a Fraude |
| Cadastro Positivo | Análise de Crédito |
| Cobrança as a Service | Cobrança |

Clientes simulados pertencem aos setores: Financeiro, Varejo, Telecom, E-commerce e Seguros.

## Como Executar

Pré-requisitos:

```bash
pip install pandas matplotlib seaborn
```

Passo a passo:

```bash
python 1_simulacao_limpeza.py
python 2_analise_exploratoria.py
```

As consultas SQL podem ser executadas em qualquer banco SQLite/DuckDB/PostgreSQL com a tabela data_clean carregada.

## Suposições e Decisões

- Período: 01/01/2023 a 31/12/2023, conforme enunciado. A consulta SQL de junho foi adaptada para 2023, pois o dataset não cobre 2024; a lógica de filtragem é idêntica.
- Produtos: baseados no portfólio público da Quod (Score PF/PJ, Quod X, Quod Identity, Cadastro Positivo, Cobrança as a Service).
- Sazonalidade: Q4 modela o aumento real de demanda por crédito e antifraude em períodos de alta (Black Friday, Natal).
- Imperfeições inseridas: valores nulos (8%), strings inválidas em colunas numéricas e 5 duplicatas, para demonstrar técnicas reais de limpeza.
- Preenchimento de nulos: mediana por produto, mais robusto que média para dados com outliers de preço.

## Principais Resultados

- Produto campeão em receita: Quod X Antifraude (R$ 185k)
- Produto campeão em volume: Quod Score PF
- Sazonalidade Q4: +72% acima da média trimestral
- Setor de maior receita: Seguros
