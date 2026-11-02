"""Abertura e inicialização do banco SQLite do Ranking Match."""

import sqlite3
from pathlib import Path

_PASTA = Path(__file__).resolve().parent

CAMINHO_PADRAO: Path = _PASTA / "ranking_match.db"

_SCHEMA = _PASTA / "schema.sql"
_SEED = _PASTA / "seed.sql"
# Perfis fictícios com listas preenchidas, para a demonstração do app.
_MOCK = _PASTA / "mock.sql"
# Marca, no PRAGMA user_version, que o mock já foi aplicado neste banco.
_VERSAO_MOCK = 1


def conectar(
    caminho: str | Path | None = None, com_mock: bool = True
) -> sqlite3.Connection:
    """Abre a conexão com o banco, já inicializado com schema, seed e mock.

    ``caminho`` None usa :data:`CAMINHO_PADRAO`; aceita também ``":memory:"``.
    ``com_mock=False`` deixa de fora os perfis fictícios (usado nos testes).
    """
    destino = CAMINHO_PADRAO if caminho is None else caminho
    conn = sqlite3.connect(destino)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    inicializar(conn, com_mock)
    return conn


def inicializar(conn: sqlite3.Connection, com_mock: bool = True) -> None:
    """Executa schema.sql, seed.sql e, se pedido, mock.sql.

    Pode ser chamada várias vezes. Schema e seed usam IF NOT EXISTS e INSERT OR
    IGNORE. O mock só roda uma vez, num banco ainda sem listas salvas: depois
    disso as listas são das pessoas, e reaplicar o mock traria de volta itens
    que elas tiraram.
    """
    conn.executescript(_SCHEMA.read_text(encoding="utf-8"))
    conn.executescript(_SEED.read_text(encoding="utf-8"))
    if com_mock and _mock_pendente(conn):
        conn.executescript(_MOCK.read_text(encoding="utf-8"))
        conn.execute(f"PRAGMA user_version = {_VERSAO_MOCK}")
    conn.commit()


def _mock_pendente(conn: sqlite3.Connection) -> bool:
    """True se o mock ainda não foi aplicado e ninguém salvou lista."""
    versao = conn.execute("PRAGMA user_version").fetchone()[0]
    tem_ranking = conn.execute("SELECT 1 FROM ranking LIMIT 1").fetchone()
    return versao < _VERSAO_MOCK and tem_ranking is None
