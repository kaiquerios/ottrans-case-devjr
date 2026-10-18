
# Análise da Demanda de Ônibus

Projeto de ETL e análise de dados desenvolvido para o teste técnico de Desenvolvedor de Sistemas Júnior.

## Objetivo

Extrair, tratar, armazenar e analisar dados públicos de demanda de transporte por ônibus, disponibilizando indicadores e visualizações interativas.

## Tecnologias

- Python
- Pandas
- SQLite
- SQL
- Streamlit
- Plotly
- Pytest

## Fonte dos dados

Portal Brasileiro de Dados Abertos:

https://dados.gov.br/dados/conjuntos-dados/demanda

Arquivos utilizados:
- `demanda_202201.csv`
- `demanda_202202.csv`

O conjunto analisado contém dados de janeiro e fevereiro de 2022.

## Pipeline ETL

1. Leitura dos arquivos CSV.
2. Padronização dos nomes das colunas.
3. Normalização dos formatos de data.
4. Remoção de espaços extras em campos textuais.
5. Conversão dos campos numéricos.
6. Validação das datas e da demanda.
7. Consolidação dos arquivos.
8. Armazenamento no SQLite.

## Qualidade dos dados

- O arquivo de janeiro não possui cabeçalho; os nomes das colunas são atribuídos durante a leitura.
- Os arquivos utilizam formatos de data diferentes; cada arquivo é interpretado explicitamente antes da padronização.
- Espaços extras nos campos textuais são removidos.

Após o tratamento, foram consolidados 166.582 registros.

## Banco de dados

Foi utilizado SQLite por ser leve, local e não exigir servidor separado, facilitando a reprodução do projeto.

## Consultas SQL

O arquivo `consultas.sql` contém cinco análises:
- Demanda total por mês.
- Dez linhas com maior demanda.
- Demanda por tipo de passageiro.
- Demanda média por linha.
- Demanda por dia da semana.

## Dashboard

O dashboard permite filtrar o período e o tipo de passageiro e apresenta indicadores, gráficos e uma tabela das linhas com maior demanda.

## Como executar

Instale as dependências:

```bash
python -m pip install -r requirements.txt
```

Execute o ETL:

```bash
python script.py
```

Execute as consultas SQL:

```bash
python consultas.py
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

Os cinco testes verificam:
- Quantidade de registros processados.
- Colunas esperadas.
- Persistência dos dados no SQLite.
- Ausência de demanda negativa.
- Período das datas processadas.S

## Limitações

Os dados utilizados cobrem somente janeiro e fevereiro de 2022. Os códigos de tipo de passageiro são apresentados conforme encontrados na fonte, sem atribuição de descrições não confirmadas.
