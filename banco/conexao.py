"""Abertura e inicialização do banco SQLite do Ranking Match."""

import sqlite3
from pathlib import Path

_PASTA = Path(__file__).resolve().parent

CAMINHO_PADRAO: Path = _PASTA / "ranking_match.db"

_SCHEMA = _PASTA / "schema.sql"
_SEED = _PASTA / "seed.sql"


def conectar(caminho: str | Path | None = None) -> sqlite3.Connection:
    """Abre a conexão com o banco, já inicializado com schema e seed.

    ``caminho`` None usa :data:`CAMINHO_PADRAO`; aceita também ``":memory:"``.
    """
    destino = CAMINHO_PADRAO if caminho is None else caminho
    conn = sqlite3.connect(destino)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    inicializar(conn)
    return conn


def inicializar(conn: sqlite3.Connection) -> None:
    """Executa schema.sql e seed.sql. Pode ser chamada várias vezes."""
    conn.executescript(_SCHEMA.read_text(encoding="utf-8"))
    conn.executescript(_SEED.read_text(encoding="utf-8"))
    conn.commit()
