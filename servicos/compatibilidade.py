"""Aba Compatibilidade: compara rankings contando inversões."""

import sqlite3

from algoritmos.inversoes import contar_inversoes
from banco.repositorio import listar_pessoas, obter_ranking, pessoas_com_ranking


def compatibilidade(
    conn: sqlite3.Connection,
    pessoa_a_id: int,
    pessoa_b_id: int,
    categoria_id: int,
) -> dict:
    """Mede a compatibilidade entre duas pessoas em uma categoria.

    Devolve ``{"inversoes", "total_pares", "percentual"}``. Rankings idênticos
    dão 100.0 e rankings exatamente invertidos dão 0.0.
    """
    if pessoa_a_id == pessoa_b_id:
        raise ValueError("Escolha duas pessoas diferentes para comparar.")

    ranking_a = _exigir_ranking(conn, pessoa_a_id, categoria_id)
    ranking_b = _exigir_ranking(conn, pessoa_b_id, categoria_id)

    if set(ranking_a) != set(ranking_b):
        raise ValueError("Os dois rankings não cobrem os mesmos itens da categoria.")

    posicao_em_b = {item_id: posicao for posicao, item_id in enumerate(ranking_b)}

    # Percorrendo os itens na ordem de A, cada inversão na sequência das posições
    # de B é um par em que as duas pessoas discordam.
    sequencia = [posicao_em_b[item_id] for item_id in ranking_a]
    inversoes, _ = contar_inversoes(sequencia)

    n = len(ranking_a)
    total_pares = n * (n - 1) // 2
    percentual = 100.0 if total_pares == 0 else 100 * (1 - inversoes / total_pares)

    return {
        "inversoes": inversoes,
        "total_pares": total_pares,
        "percentual": round(percentual, 1),
    }


def ranking_compatibilidade(
    conn: sqlite3.Connection, pessoa_id: int, categoria_id: int
) -> list[dict]:
    """Compara a pessoa com todas as outras que têm ranking na categoria.

    Devolve ``[{"pessoa_id", "nome", "inversoes", "percentual"}, ...]`` em ordem
    decrescente de percentual (empate: nome crescente).
    """
    _exigir_ranking(conn, pessoa_id, categoria_id)

    resultados: list[dict] = []
    for outra in pessoas_com_ranking(conn, categoria_id):
        if outra["id"] == pessoa_id:
            continue
        medida = compatibilidade(conn, pessoa_id, outra["id"], categoria_id)
        resultados.append(
            {
                "pessoa_id": outra["id"],
                "nome": outra["nome"],
                "inversoes": medida["inversoes"],
                "percentual": medida["percentual"],
            }
        )

    resultados.sort(key=lambda linha: (-linha["percentual"], linha["nome"]))
    return resultados


def _exigir_ranking(
    conn: sqlite3.Connection, pessoa_id: int, categoria_id: int
) -> list[int]:
    """Devolve o ranking da pessoa ou levanta ValueError se ela não tiver um."""
    ranking = obter_ranking(conn, pessoa_id, categoria_id)
    if not ranking:
        nome = _nome_da_pessoa(conn, pessoa_id)
        raise ValueError(f"{nome} ainda não ordenou os itens dessa categoria.")
    return ranking


def _nome_da_pessoa(conn: sqlite3.Connection, pessoa_id: int) -> str:
    """Nome da pessoa, para usar nas mensagens de erro."""
    for pessoa in listar_pessoas(conn):
        if pessoa["id"] == pessoa_id:
            return str(pessoa["nome"])
    raise ValueError("Pessoa não encontrada.")
