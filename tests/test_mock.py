"""Testes dos perfis mockados (banco/mock.sql)."""

import sqlite3
from collections.abc import Iterator
from pathlib import Path

import pytest

from banco.conexao import conectar
from banco.repositorio import (
    listar_pessoas,
    obter_ranking,
    pessoas_com_ranking,
    salvar_ranking,
)


@pytest.fixture
def conn_mock() -> Iterator[sqlite3.Connection]:
    """Conexão em memória com seed e mock."""
    conexao = conectar(":memory:")
    try:
        yield conexao
    finally:
        conexao.close()


def test_mock_carrega_dez_pessoas_com_listas(conn_mock: sqlite3.Connection) -> None:
    assert len(listar_pessoas(conn_mock)) == 10

    for categoria_id in (1, 2, 3):
        assert len(pessoas_com_ranking(conn_mock, categoria_id)) == 10


def test_mock_tem_nota_para_todas_as_pessoas(conn_mock: sqlite3.Connection) -> None:
    total = conn_mock.execute("SELECT COUNT(*) FROM nota").fetchone()[0]

    assert total == 10 * 3


def test_mock_sem_posicao_repetida(conn_mock: sqlite3.Connection) -> None:
    repetidas = conn_mock.execute(
        """
        SELECT COUNT(*) FROM (
            SELECT ranking.pessoa_id, item.categoria_id, ranking.posicao
              FROM ranking
              JOIN item ON item.id = ranking.item_id
             GROUP BY 1, 2, 3
            HAVING COUNT(*) > 1
        )
        """
    ).fetchone()[0]

    assert repetidas == 0


def test_mock_nao_volta_depois_de_editar(tmp_path: Path) -> None:
    caminho = tmp_path / "teste.db"

    conexao = conectar(caminho)
    salvar_ranking(conexao, 1, 2, [54, 58])
    conexao.close()

    # Reconectar (como acontece a cada rerun do Streamlit) não reaplica o mock.
    conexao = conectar(caminho)
    assert obter_ranking(conexao, 1, 2) == [54, 58]
    conexao.close()


def test_sem_mock_fica_so_a_seed() -> None:
    conexao = conectar(":memory:", com_mock=False)

    assert len(listar_pessoas(conexao)) == 6
    assert conexao.execute("SELECT COUNT(*) FROM ranking").fetchone()[0] == 0
    conexao.close()
