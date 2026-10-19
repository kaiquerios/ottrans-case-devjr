import sqlite3
from pathlib import Path

import pandas as pd

RAIZ = Path(__file__).resolve().parents[1]
DADOS_BRUTOS = RAIZ / "data" / "raw"
DADOS_TRATADOS = RAIZ / "data" / "processed"
BANCO = RAIZ / "data" / "database" / "demanda.db"

COLUNAS = [
    "DataMovimento",
    "CodLinha",
    "NomeLinha",
    "TipoPassageiro",
    "NomePassageiro",
    "Demanda",
]


def carregar_arquivo(arquivo, tem_cabecalho, formato_data):
    if tem_cabecalho:
        df = pd.read_csv(
            arquivo,
            sep=";",
            encoding="utf-8-sig",
        )
    else:
        df = pd.read_csv(
            arquivo,
            sep=";",
            encoding="utf-8-sig",
            header=None,
            names=COLUNAS,
        )

    df.columns = df.columns.str.strip()

    for coluna in ["NomeLinha", "NomePassageiro"]:
        df[coluna] = df[coluna].astype("string").str.strip()

    df["DataMovimento"] = pd.to_datetime(
        df["DataMovimento"],
        format=formato_data,
        errors="coerce",
    )

    for coluna in ["CodLinha", "TipoPassageiro", "Demanda"]:
        df[coluna] = pd.to_numeric(df[coluna], errors="coerce")

    return df[COLUNAS]


def executar_etl():
    janeiro = carregar_arquivo(
        DADOS_BRUTOS / "demanda_202201.csv", False, "%Y-%m-%d"
    )
    fevereiro = carregar_arquivo(
        DADOS_BRUTOS / "demanda_202202.csv", True, "%d/%m/%Y"
    )

    base = pd.concat([janeiro, fevereiro], ignore_index=True)

    assert base["DataMovimento"].notna().all()
    assert base["CodLinha"].notna().all()
    assert base["TipoPassageiro"].notna().all()
    assert base["Demanda"].notna().all()
    assert (base["Demanda"] >= 0).all()

    base["DataMovimento"] = base["DataMovimento"].dt.strftime("%Y-%m-%d")

    return base


def salvar_sqlite(base):
    BANCO.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(BANCO) as conexao:
        base.to_sql(
            "demanda",
            conexao,
            if_exists="replace",
            index=False,
        )

        total = pd.read_sql_query(
            "SELECT COUNT(*) AS total FROM demanda",
            conexao,
        )

        print(f"Banco criado: {BANCO.relative_to(RAIZ)}")
        print("Registros gravados:", total.loc[0, "total"])


if __name__ == "__main__":
    base = executar_etl()
    DADOS_TRATADOS.mkdir(parents=True, exist_ok=True)
    base.to_csv(DADOS_TRATADOS / "demanda_tratada.csv", index=False, encoding="utf-8")
    salvar_sqlite(base)

    print("ETL concluído.")
    print("Registros processados:", len(base))
