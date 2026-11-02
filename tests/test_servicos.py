"""Testes da camada de serviços que a interface vai chamar."""

import math
import sqlite3

import pytest

from banco.repositorio import criar_pessoa, salvar_ranking
from servicos.compatibilidade import compatibilidade, ranking_compatibilidade
from servicos.dupla import dupla_mais_parecida

ORDEM_BASE = [1, 2, 3, 4, 5, 6, 7, 8]
ORDEM_INVERTIDA = [8, 7, 6, 5, 4, 3, 2, 1]

ANA, BRUNO, CARLA, DIEGO, ELISA = 1, 2, 3, 4, 5


# --- Dupla mais parecida -------------------------------------------------


@pytest.mark.parametrize(
    "categoria_id, nome_a, nome_b, distancia",
    [
        (1, "Bruno", "Diego", math.sqrt(2)),
        (2, "Ana", "Carla", math.sqrt(2)),
        (3, "Ana", "Diego", 2.0),
    ],
)
def test_dupla_mais_parecida_com_a_seed(
    conn: sqlite3.Connection,
    categoria_id: int,
    nome_a: str,
    nome_b: str,
    distancia: float,
) -> None:
    resultado = dupla_mais_parecida(conn, categoria_id)

    assert resultado["pessoa_a"]["nome"] == nome_a
    assert resultado["pessoa_b"]["nome"] == nome_b
    assert math.isclose(resultado["distancia"], distancia)
    assert resultado["pessoa_a"]["id"] < resultado["pessoa_b"]["id"]
    assert set(resultado["pessoa_a"]) == {"id", "nome", "x", "y"}


def test_dupla_mais_parecida_sem_notas(conn: sqlite3.Connection) -> None:
    conn.execute("DELETE FROM nota WHERE categoria_id = 1")
    conn.commit()

    with pytest.raises(ValueError, match="pelo menos 2 pessoas com nota"):
        dupla_mais_parecida(conn, 1)


def test_dupla_mais_parecida_com_uma_pessoa_so(conn: sqlite3.Connection) -> None:
    conn.execute("DELETE FROM nota WHERE categoria_id = 1 AND pessoa_id > 1")
    conn.commit()

    with pytest.raises(ValueError, match="pelo menos 2 pessoas com nota"):
        dupla_mais_parecida(conn, 1)


# --- Compatibilidade -----------------------------------------------------


def test_compatibilidade_rankings_identicos(conn: sqlite3.Connection) -> None:
    salvar_ranking(conn, ANA, 1, ORDEM_BASE)
    salvar_ranking(conn, BRUNO, 1, ORDEM_BASE)

    assert compatibilidade(conn, ANA, BRUNO, 1) == {
        "em_comum": 8,
        "escolhidos": 8,
        "inversoes": 0,
        "total_pares": 28,
        "percentual": 100.0,
    }


def test_compatibilidade_rankings_invertidos(conn: sqlite3.Connection) -> None:
    salvar_ranking(conn, ANA, 1, ORDEM_BASE)
    salvar_ranking(conn, BRUNO, 1, ORDEM_INVERTIDA)

    assert compatibilidade(conn, ANA, BRUNO, 1) == {
        "em_comum": 8,
        "escolhidos": 8,
        "inversoes": 28,
        "total_pares": 28,
        "percentual": 0.0,
    }


def test_compatibilidade_caso_intermediario(conn: sqlite3.Connection) -> None:
    # Trocar os 3 primeiros itens de ordem gera 3 inversões (os pares 1-2, 1-3
    # e 2-3). 100 * (1 - 3/28) = 89.2857... -> 89.3
    salvar_ranking(conn, ANA, 1, ORDEM_BASE)
    salvar_ranking(conn, BRUNO, 1, [3, 2, 1, 4, 5, 6, 7, 8])

    assert compatibilidade(conn, ANA, BRUNO, 1) == {
        "em_comum": 8,
        "escolhidos": 8,
        "inversoes": 3,
        "total_pares": 28,
        "percentual": 89.3,
    }


def test_compatibilidade_troca_de_vizinhos(conn: sqlite3.Connection) -> None:
    # Uma única troca de vizinhos = 1 inversão. 100 * (1 - 1/28) = 96.4285... -> 96.4
    salvar_ranking(conn, ANA, 1, ORDEM_BASE)
    salvar_ranking(conn, BRUNO, 1, [2, 1, 3, 4, 5, 6, 7, 8])

    assert compatibilidade(conn, ANA, BRUNO, 1) == {
        "em_comum": 8,
        "escolhidos": 8,
        "inversoes": 1,
        "total_pares": 28,
        "percentual": 96.4,
    }


def test_compatibilidade_e_simetrica(conn: sqlite3.Connection) -> None:
    salvar_ranking(conn, ANA, 1, ORDEM_BASE)
    salvar_ranking(conn, BRUNO, 1, [3, 2, 1, 8, 5, 6, 7, 4])

    assert compatibilidade(conn, ANA, BRUNO, 1) == compatibilidade(
        conn, BRUNO, ANA, 1
    )


def test_compatibilidade_parcial_com_inversao(conn: sqlite3.Connection) -> None:
    # Em comum, na ordem de Ana: [1, 2, 3]. Posições de Bruno: [1, 0, 2] -> 1
    # inversão (o par 1-2) em 3 pares. Escolhidos por algum: {1, 2, 3, 4, 5}.
    # 100 * (3/5) * (1 - 1/3) = 40.0
    salvar_ranking(conn, ANA, 1, [1, 2, 3, 4])
    salvar_ranking(conn, BRUNO, 1, [2, 1, 3, 5])

    assert compatibilidade(conn, ANA, BRUNO, 1) == {
        "em_comum": 3,
        "escolhidos": 5,
        "inversoes": 1,
        "total_pares": 3,
        "percentual": 40.0,
    }


def test_compatibilidade_parcial_mesma_ordem(conn: sqlite3.Connection) -> None:
    # Bruno concorda na ordem, mas só escolheu 3 dos 4 itens de Ana: 100 * 3/4.
    salvar_ranking(conn, ANA, 1, [1, 2, 3, 4])
    salvar_ranking(conn, BRUNO, 1, [1, 2, 3])

    assert compatibilidade(conn, ANA, BRUNO, 1)["percentual"] == 75.0


def test_compatibilidade_um_item_em_comum(conn: sqlite3.Connection) -> None:
    # Com 1 item em comum não há par para discordar: só a sobreposição (1/3).
    salvar_ranking(conn, ANA, 1, [1, 2])
    salvar_ranking(conn, BRUNO, 1, [2, 3])

    resultado = compatibilidade(conn, ANA, BRUNO, 1)

    assert (resultado["em_comum"], resultado["total_pares"]) == (1, 0)
    assert resultado["percentual"] == 33.3


def test_compatibilidade_nada_em_comum(conn: sqlite3.Connection) -> None:
    salvar_ranking(conn, ANA, 1, [1, 2, 3])
    salvar_ranking(conn, BRUNO, 1, [4, 5])

    assert compatibilidade(conn, ANA, BRUNO, 1) == {
        "em_comum": 0,
        "escolhidos": 5,
        "inversoes": 0,
        "total_pares": 0,
        "percentual": 0.0,
    }


def test_compatibilidade_parcial_e_simetrica(conn: sqlite3.Connection) -> None:
    salvar_ranking(conn, ANA, 1, [8, 1, 2, 3, 4])
    salvar_ranking(conn, BRUNO, 1, [2, 1, 3, 5, 8])

    assert compatibilidade(conn, ANA, BRUNO, 1) == compatibilidade(
        conn, BRUNO, ANA, 1
    )


def test_compatibilidade_sem_ranking(conn: sqlite3.Connection) -> None:
    salvar_ranking(conn, ANA, 1, ORDEM_BASE)

    with pytest.raises(ValueError, match="Bruno"):
        compatibilidade(conn, ANA, BRUNO, 1)

    with pytest.raises(ValueError, match="Ana"):
        compatibilidade(conn, ANA, BRUNO, 2)


def test_compatibilidade_mesma_pessoa(conn: sqlite3.Connection) -> None:
    salvar_ranking(conn, ANA, 1, ORDEM_BASE)

    with pytest.raises(ValueError, match="duas pessoas diferentes"):
        compatibilidade(conn, ANA, ANA, 1)


# --- Ranking de compatibilidade ------------------------------------------


def test_ranking_compatibilidade_ordenado(conn: sqlite3.Connection) -> None:
    salvar_ranking(conn, ANA, 1, ORDEM_BASE)
    salvar_ranking(conn, BRUNO, 1, ORDEM_BASE)
    salvar_ranking(conn, ELISA, 1, ORDEM_BASE)
    salvar_ranking(conn, CARLA, 1, [3, 2, 1, 4, 5, 6, 7, 8])
    salvar_ranking(conn, DIEGO, 1, ORDEM_INVERTIDA)

    resultado = ranking_compatibilidade(conn, ANA, 1)

    assert [(linha["nome"], linha["percentual"]) for linha in resultado] == [
        ("Bruno", 100.0),  # empate em 100.0 resolvido pelo nome
        ("Elisa", 100.0),
        ("Carla", 89.3),
        ("Diego", 0.0),
    ]
    assert set(resultado[0]) == {
        "pessoa_id",
        "nome",
        "em_comum",
        "inversoes",
        "percentual",
    }
    assert resultado[-1]["inversoes"] == 28


def test_ranking_compatibilidade_nao_inclui_a_propria_pessoa(
    conn: sqlite3.Connection,
) -> None:
    salvar_ranking(conn, ANA, 1, ORDEM_BASE)
    salvar_ranking(conn, BRUNO, 1, ORDEM_BASE)

    resultado = ranking_compatibilidade(conn, ANA, 1)

    assert [linha["pessoa_id"] for linha in resultado] == [BRUNO]


def test_ranking_compatibilidade_sem_mais_ninguem(conn: sqlite3.Connection) -> None:
    salvar_ranking(conn, ANA, 1, ORDEM_BASE)

    assert ranking_compatibilidade(conn, ANA, 1) == []


def test_ranking_compatibilidade_sem_ranking_da_pessoa(
    conn: sqlite3.Connection,
) -> None:
    pessoa_id = criar_pessoa(conn, "Gabriela")

    with pytest.raises(ValueError, match="Gabriela"):
        ranking_compatibilidade(conn, pessoa_id, 1)
