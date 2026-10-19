# Análise da Demanda de Ônibus

Projeto de ETL, consultas SQL e dashboard desenvolvido para o teste técnico de Desenvolvedor de Sistemas Júnior.

**Dashboard público:** https://ottrans-case-devjr.streamlit.app/

## Estrutura do projeto

```text
ottrans-case-devjr/
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
├── .streamlit/
│   └── config.toml
├── data/
│   ├── raw/                 # CSVs originais, preservados sem alteração
│   ├── processed/           # CSV consolidado e tratado
│   └── database/            # Banco SQLite utilizado pelo dashboard
├── scripts/
│   ├── etl.py               # Leitura, tratamento e carga dos dados
│   ├── consultas.py         # Executa as consultas SQL
│   └── consultas.sql        # Consultas analíticas
└── tests/
    └── test_etl.py          # Testes automatizados
```

## Objetivo

Tratar e consolidar dados públicos de demanda de transporte por ônibus, armazená-los em SQLite e apresentar indicadores e visualizações interativas.

## Fonte dos dados

Portal Brasileiro de Dados Abertos:  
https://dados.gov.br/dados/conjuntos-dados/demanda

Arquivos usados:
- `data/raw/demanda_202201.csv`
- `data/raw/demanda_202202.csv`

O conjunto processado cobre janeiro e fevereiro de 2022 e contém 166.582 registros.

## Pipeline ETL

1. Lê os CSVs originais em `data/raw/`.
2. Define os nomes das colunas do arquivo de janeiro, que não possui cabeçalho.
3. Interpreta explicitamente os formatos de data de cada arquivo e padroniza as datas.
4. Remove espaços extras dos campos textuais.
5. Converte campos numéricos e valida datas, códigos e demanda.
6. Consolida os meses e grava o CSV tratado em `data/processed/`.
7. Carrega os registros na tabela `demanda` do banco `data/database/demanda.db`.

Os arquivos em `data/raw/` são mantidos como origem; o ETL gera novamente os arquivos derivados.

## Qualidade dos dados

- **Cabeçalho ausente em janeiro:** os nomes canônicos das seis colunas são atribuídos durante a leitura.
- **Formatos de data diferentes:** cada arquivo é interpretado com seu formato conhecido antes de padronizar as datas.
- **Espaços extras em texto:** espaços nas extremidades de `NomeLinha` e `NomePassageiro` são removidos.
- As validações verificam datas e campos numéricos obrigatórios, além de impedir demanda negativa. Não se afirma a existência de nulos ou duplicatas quando eles não foram identificados.

## Banco de dados

Foi escolhido SQLite por ser relacional, leve e não exigir um servidor separado. É suficiente para este volume e facilita a execução local e o deploy do dashboard.

## Consultas SQL

`scripts/consultas.sql` contém cinco análises:
- Demanda total por mês.
- Dez linhas com maior demanda.
- Demanda por tipo de passageiro.
- Demanda média por linha.
- Demanda por dia da semana.

## Dashboard

O dashboard em Streamlit apresenta três indicadores, dois gráficos, uma tabela com as dez linhas de maior demanda e filtros por período e tipo de passageiro.

## Como executar localmente

Na raiz do projeto, crie e ative um ambiente virtual. Depois instale as dependências:

```bash
python -m venv .venv
# Windows PowerShell:
.venv\Scripts\Activate.ps1
# Git Bash:
source .venv/Scripts/activate

python -m pip install -r requirements.txt
```

Execute o ETL para recriar os arquivos derivados e o banco:

```bash
python scripts/etl.py
```

Execute as consultas:

```bash
python scripts/consultas.py
```

Inicie o dashboard:

```bash
python -m streamlit run app.py
```

Execute os testes:

```bash
python -m pytest -v
```

## Testes automatizados

Os testes verificam a quantidade de registros, as colunas esperadas, a existência e o conteúdo do banco, a ausência de demanda negativa e o período coberto pelos dados.

## Limitações

A análise cobre apenas janeiro e fevereiro de 2022. Os códigos de tipo de passageiro são exibidos como códigos, sem atribuir descrições que não tenham sido confirmadas pela fonte.
