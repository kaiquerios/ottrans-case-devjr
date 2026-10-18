import sqlite3
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

PASTA = Path(__file__).parent
BANCO = PASTA / "demanda.db"

st.set_page_config(
    page_title="Análise da Demanda de Ônibus",
    page_icon="📊",
    layout="wide",
)

st.title("Análise da Demanda de Ônibus")
st.caption("Dados de janeiro e fevereiro de 2022")

@st.cache_data
def carregar_dados():
    with sqlite3.connect(BANCO) as conexao:
        df = pd.read_sql_query(
            "SELECT * FROM demanda",
            conexao,
        )

    df["DataMovimento"] = pd.to_datetime(
        df["DataMovimento"],
        errors="coerce",
    )

    return df

try:
    df = carregar_dados()

    if df.empty:
        st.warning("O banco de dados não contém registros.")
        st.stop()

except (sqlite3.Error, OSError) as erro:
    st.error(f"Não foi possível carregar o banco: {erro}")
    st.stop()

# Filtros
st.sidebar.header("Filtros")

data_min = df["DataMovimento"].min().date()
data_max = df["DataMovimento"].max().date()

periodo = st.sidebar.date_input(
    "Período",
    value=(data_min, data_max),
    min_value=data_min,
    max_value=data_max,
)

tipos = sorted(df["TipoPassageiro"].dropna().unique().tolist())

tipos_selecionados = st.sidebar.multiselect(
    "Tipo de passageiro",
    options=tipos,
    default=tipos,
)

filtrado = df.copy()

if isinstance(periodo, (tuple, list)) and len(periodo) == 2:
    inicio, fim = periodo
    filtrado = filtrado[
        filtrado["DataMovimento"].dt.date.between(inicio, fim)
    ]

if tipos_selecionados:
    filtrado = filtrado[
        filtrado["TipoPassageiro"].isin(tipos_selecionados)
    ]
else:
    filtrado = filtrado.iloc[0:0]

if filtrado.empty:
    st.warning("Nenhum registro encontrado para os filtros selecionados.")
    st.stop()

# Indicadores
demanda_total = int(filtrado["Demanda"].sum())
linhas_total = filtrado["CodLinha"].nunique()
demanda_media = filtrado["Demanda"].mean()

col1, col2, col3 = st.columns(3)

col1.metric("Demanda total", f"{demanda_total:,}".replace(",", "."))
col2.metric("Linhas de ônibus", f"{linhas_total:,}".replace(",", "."))
col3.metric("Demanda média por registro", f"{demanda_media:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))

# Preparar gráficos
por_dia = (
    filtrado.assign(
        DataMovimento=filtrado["DataMovimento"].dt.date
    )
    .groupby("DataMovimento", as_index=False)["Demanda"]
    .sum()
)

por_tipo = (
    filtrado.groupby("TipoPassageiro", as_index=False)["Demanda"]
    .sum()
    .sort_values("Demanda", ascending=False)
)

col_grafico1, col_grafico2 = st.columns(2)

with col_grafico1:
    st.subheader("Demanda ao longo do tempo")
    figura_dias = px.line(
        por_dia,
        x="DataMovimento",
        y="Demanda",
        markers=True,
        labels={
            "DataMovimento": "Data",
            "Demanda": "Demanda total",
        },
    )
    st.plotly_chart(figura_dias, use_container_width=True)

with col_grafico2:
    st.subheader("Demanda por tipo de passageiro")
    figura_tipos = px.bar(
        por_tipo,
        x="TipoPassageiro",
        y="Demanda",
        labels={
            "TipoPassageiro": "Código do tipo",
            "Demanda": "Demanda total",
        },
    )
    st.plotly_chart(figura_tipos, use_container_width=True)

st.subheader("10 linhas com maior demanda")

por_linha = (
    filtrado.groupby(["CodLinha", "NomeLinha"], as_index=False)["Demanda"]
    .sum()
    .sort_values("Demanda", ascending=False)
    .head(10)
)

st.dataframe(por_linha, use_container_width=True, hide_index=True)

st.caption(
    f"Registros considerados: {len(filtrado):,}".replace(",", ".")
)
