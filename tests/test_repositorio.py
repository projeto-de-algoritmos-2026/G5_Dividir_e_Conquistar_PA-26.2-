"""Testes da camada de acesso ao banco."""

import sqlite3

import pytest

from banco.conexao import inicializar
from banco.repositorio import (
    criar_pessoa,
    listar_categorias,
    listar_itens,
    listar_notas,
    listar_pessoas,
    obter_ranking,
    pessoas_com_ranking,
    salvar_nota,
    salvar_ranking,
)


def test_seed_carregada(conn: sqlite3.Connection) -> None:
    assert len(listar_categorias(conn)) == 3
    assert len(listar_pessoas(conn)) == 6
    assert len(listar_itens(conn, 1)) == 8

    total_itens = sum(len(listar_itens(conn, c["id"])) for c in listar_categorias(conn))
    assert total_itens == 24


def test_categorias_tem_os_eixos(conn: sqlite3.Connection) -> None:
    categoria = listar_categorias(conn)[0]

    assert set(categoria) == {"id", "nome", "eixo_x", "eixo_y"}
    assert categoria["nome"] == "Jogos"


def test_inicializar_de_novo_nao_duplica(conn: sqlite3.Connection) -> None:
    inicializar(conn)
    inicializar(conn)

    assert len(listar_categorias(conn)) == 3
    assert len(listar_pessoas(conn)) == 6
    assert len(listar_itens(conn, 1)) == 8
    assert len(listar_notas(conn, 1)) == 6


def test_criar_pessoa(conn: sqlite3.Connection) -> None:
    novo_id = criar_pessoa(conn, "  Gabriela  ")

    assert isinstance(novo_id, int)
    assert {p["nome"] for p in listar_pessoas(conn)} >= {"Gabriela"}


@pytest.mark.parametrize("nome", ["", "   "])
def test_criar_pessoa_com_nome_vazio(conn: sqlite3.Connection, nome: str) -> None:
    with pytest.raises(ValueError, match="não pode ser vazio"):
        criar_pessoa(conn, nome)


def test_criar_pessoa_com_nome_duplicado(conn: sqlite3.Connection) -> None:
    with pytest.raises(ValueError, match="Já existe uma pessoa com esse nome."):
        criar_pessoa(conn, "Ana")


def test_salvar_e_obter_ranking(conn: sqlite3.Connection) -> None:
    ordem = [4, 1, 8, 2, 6, 3, 7, 5]

    salvar_ranking(conn, 1, 1, ordem)

    assert obter_ranking(conn, 1, 1) == ordem


def test_salvar_ranking_substitui_o_anterior(conn: sqlite3.Connection) -> None:
    salvar_ranking(conn, 1, 1, [1, 2, 3, 4, 5, 6, 7, 8])
    salvar_ranking(conn, 1, 1, [8, 7, 6, 5, 4, 3, 2, 1])

    assert obter_ranking(conn, 1, 1) == [8, 7, 6, 5, 4, 3, 2, 1]
    assert conn.execute("SELECT COUNT(*) FROM ranking").fetchone()[0] == 8


def test_ranking_de_categorias_diferentes_nao_se_misturam(
    conn: sqlite3.Connection,
) -> None:
    salvar_ranking(conn, 1, 1, [1, 2, 3, 4, 5, 6, 7, 8])
    salvar_ranking(conn, 1, 2, [9, 10, 11, 12, 13, 14, 15, 16])

    assert obter_ranking(conn, 1, 1) == [1, 2, 3, 4, 5, 6, 7, 8]
    assert obter_ranking(conn, 1, 2) == [9, 10, 11, 12, 13, 14, 15, 16]


def test_obter_ranking_inexistente(conn: sqlite3.Connection) -> None:
    assert obter_ranking(conn, 1, 1) == []


def test_salvar_ranking_parcial(conn: sqlite3.Connection) -> None:
    # A pessoa escolhe só os itens de que gosta, em ordem de preferência.
    salvar_ranking(conn, 1, 1, [5, 2, 7])

    assert obter_ranking(conn, 1, 1) == [5, 2, 7]


def test_salvar_ranking_vazio(conn: sqlite3.Connection) -> None:
    with pytest.raises(ValueError, match="pelo menos 1 item"):
        salvar_ranking(conn, 1, 1, [])


def test_salvar_ranking_menor_substitui_o_maior(conn: sqlite3.Connection) -> None:
    salvar_ranking(conn, 1, 1, [1, 2, 3, 4, 5, 6, 7, 8])
    salvar_ranking(conn, 1, 1, [3, 1])

    assert obter_ranking(conn, 1, 1) == [3, 1]
    assert conn.execute("SELECT COUNT(*) FROM ranking").fetchone()[0] == 2


def test_salvar_ranking_com_item_repetido(conn: sqlite3.Connection) -> None:
    with pytest.raises(ValueError, match="repetir itens"):
        salvar_ranking(conn, 1, 1, [1, 1, 2, 3, 4, 5, 6, 7])


def test_salvar_ranking_com_item_de_outra_categoria(conn: sqlite3.Connection) -> None:
    with pytest.raises(ValueError, match="não pertence à categoria"):
        salvar_ranking(conn, 1, 1, [1, 2, 3, 4, 5, 6, 7, 9])


def test_salvar_ranking_de_pessoa_inexistente(conn: sqlite3.Connection) -> None:
    with pytest.raises(ValueError, match="Pessoa não encontrada."):
        salvar_ranking(conn, 999, 1, [1, 2, 3, 4, 5, 6, 7, 8])


def test_salvar_ranking_invalido_nao_grava_nada(conn: sqlite3.Connection) -> None:
    salvar_ranking(conn, 1, 1, [1, 2, 3, 4, 5, 6, 7, 8])

    with pytest.raises(ValueError):
        salvar_ranking(conn, 1, 1, [1, 2, 9])

    assert obter_ranking(conn, 1, 1) == [1, 2, 3, 4, 5, 6, 7, 8]


def test_pessoas_com_ranking(conn: sqlite3.Connection) -> None:
    assert pessoas_com_ranking(conn, 1) == []

    salvar_ranking(conn, 2, 1, [1, 2, 3, 4, 5, 6, 7, 8])
    salvar_ranking(conn, 1, 1, [8, 7, 6, 5, 4, 3, 2, 1])

    assert pessoas_com_ranking(conn, 1) == [
        {"id": 1, "nome": "Ana"},
        {"id": 2, "nome": "Bruno"},
    ]


def test_pessoas_com_ranking_inclui_ranking_parcial(
    conn: sqlite3.Connection,
) -> None:
    salvar_ranking(conn, 1, 1, [4])

    assert pessoas_com_ranking(conn, 1) == [{"id": 1, "nome": "Ana"}]
    assert pessoas_com_ranking(conn, 2) == []


def test_salvar_nota_insere_e_atualiza(conn: sqlite3.Connection) -> None:
    pessoa_id = criar_pessoa(conn, "Gabriela")

    salvar_nota(conn, pessoa_id, 1, 1.5, 2.5)
    notas = {n["pessoa_id"]: n for n in listar_notas(conn, 1)}
    assert (notas[pessoa_id]["x"], notas[pessoa_id]["y"]) == (1.5, 2.5)

    salvar_nota(conn, pessoa_id, 1, 9.0, 0.0)
    notas = {n["pessoa_id"]: n for n in listar_notas(conn, 1)}
    assert (notas[pessoa_id]["x"], notas[pessoa_id]["y"]) == (9.0, 0.0)
    assert len(listar_notas(conn, 1)) == 7, "upsert não deve criar linha nova"


@pytest.mark.parametrize("x, y", [(-0.1, 5.0), (10.1, 5.0), (5.0, -1.0), (5.0, 11.0)])
def test_salvar_nota_fora_do_intervalo(
    conn: sqlite3.Connection, x: float, y: float
) -> None:
    with pytest.raises(ValueError, match="entre 0 e 10"):
        salvar_nota(conn, 1, 1, x, y)


def test_salvar_nota_de_pessoa_ou_categoria_inexistente(
    conn: sqlite3.Connection,
) -> None:
    with pytest.raises(ValueError, match="Pessoa não encontrada."):
        salvar_nota(conn, 999, 1, 1.0, 1.0)

    with pytest.raises(ValueError, match="Categoria não encontrada."):
        salvar_nota(conn, 1, 999, 1.0, 1.0)


def test_listar_notas_ordenado_por_pessoa(conn: sqlite3.Connection) -> None:
    notas = listar_notas(conn, 1)

    assert [n["pessoa_id"] for n in notas] == [1, 2, 3, 4, 5, 6]
    assert set(notas[0]) == {"pessoa_id", "nome", "x", "y"}
    assert notas[0]["nome"] == "Ana"
