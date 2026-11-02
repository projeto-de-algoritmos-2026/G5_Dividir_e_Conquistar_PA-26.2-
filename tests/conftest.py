"""Fixtures compartilhadas pelos testes."""

import sqlite3
import sys
from collections.abc import Iterator
from pathlib import Path

import pytest

# Garante que a raiz do repo esteja no sys.path, para os testes encontrarem
# banco/, algoritmos/ e servicos/ mesmo rodando com `pytest` em vez de
# `python -m pytest`.
RAIZ = Path(__file__).resolve().parent.parent
if str(RAIZ) not in sys.path:
    sys.path.insert(0, str(RAIZ))

from banco.conexao import conectar  # noqa: E402


@pytest.fixture
def conn() -> Iterator[sqlite3.Connection]:
    """Conexão em memória já inicializada com schema.sql e seed.sql."""
    conexao = conectar(":memory:")
    try:
        yield conexao
    finally:
        conexao.close()
