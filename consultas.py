import sqlite3
from pathlib import Path

BANCO = Path(__file__).parent / "demanda.db"
ARQUIVO_SQL = Path(__file__).parent / "consultas.sql"

with sqlite3.connect(BANCO) as conexao:
    consultas = ARQUIVO_SQL.read_text(encoding="utf-8")
    blocos = [
        bloco.strip()
        for bloco in consultas.split(";")
        if bloco.strip()
    ]

    for numero, sql in enumerate(blocos, start=1):
        print(f"\n{'=' * 50}")
        print(f"CONSULTA {numero}")
        print("=" * 50)

        cursor = conexao.execute(sql)
        colunas = [item[0] for item in cursor.description]
        linhas = cursor.fetchall()

        print(" | ".join(colunas))
        for linha in linhas:
            print(" | ".join(str(valor) for valor in linha))
