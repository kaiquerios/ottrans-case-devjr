import sqlite3
import sys
from pathlib import Path

import pandas as pd

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "scripts"))
from etl import executar_etl

BANCO = RAIZ / "data" / "database" / "demanda.db"


def test_etl_retorna_registros():
    df = executar_etl()

    assert not df.empty
    assert len(df) == 166582


def test_etl_tem_colunas_esperadas():
    df = executar_etl()

    colunas_esperadas = [
        "DataMovimento",
        "CodLinha",
        "NomeLinha",
        "TipoPassageiro",
        "NomePassageiro",
        "Demanda",
    ]

    assert list(df.columns) == colunas_esperadas


def test_banco_sqlite_tem_registros():
    assert BANCO.exists()

    with sqlite3.connect(BANCO) as conexao:
        resultado = pd.read_sql_query(
            "SELECT COUNT(*) AS total FROM demanda",
            conexao,
        )

    assert resultado.loc[0, "total"] == 166582


def test_demanda_nao_e_negativa():
    df = executar_etl()

    assert (df["Demanda"] >= 0).all()


def test_datas_estao_no_periodo_esperado():
    df = executar_etl()

    datas = pd.to_datetime(df["DataMovimento"])

    assert datas.min() == pd.Timestamp("2022-01-01")
    assert datas.max() == pd.Timestamp("2022-02-28")
