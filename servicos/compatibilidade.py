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

    Cada pessoa escolheu só os itens de que gosta, em ordem de preferência. A
    compatibilidade junta duas coisas:

    - **sobreposição**: itens em comum / itens escolhidos por pelo menos um;
    - **concordância**: 1 − inversões / pares, contando as inversões (por
      divisão e conquista) só entre os itens em comum.

    ``percentual = 100 × sobreposição × concordância``. Com menos de 2 itens em
    comum não há par para discordar e a concordância vale 1.

    Devolve ``{"em_comum", "escolhidos", "inversoes", "total_pares",
    "percentual"}``.
    """
    if pessoa_a_id == pessoa_b_id:
        raise ValueError("Escolha duas pessoas diferentes para comparar.")

    ranking_a = _exigir_ranking(conn, pessoa_a_id, categoria_id)
    ranking_b = _exigir_ranking(conn, pessoa_b_id, categoria_id)

    posicao_em_b = {item_id: posicao for posicao, item_id in enumerate(ranking_b)}
    em_comum = [item_id for item_id in ranking_a if item_id in posicao_em_b]
    escolhidos = len(set(ranking_a) | set(ranking_b))

    # Percorrendo os itens em comum na ordem de A, cada inversão na sequência
    # das posições de B é um par em que as duas pessoas discordam.
    sequencia = [posicao_em_b[item_id] for item_id in em_comum]
    inversoes, _ = contar_inversoes(sequencia)

    n = len(em_comum)
    total_pares = n * (n - 1) // 2
    concordancia = 1.0 if total_pares == 0 else 1 - inversoes / total_pares
    sobreposicao = n / escolhidos

    return {
        "em_comum": n,
        "escolhidos": escolhidos,
        "inversoes": inversoes,
        "total_pares": total_pares,
        "percentual": round(100 * sobreposicao * concordancia, 1),
    }


def ranking_compatibilidade(
    conn: sqlite3.Connection, pessoa_id: int, categoria_id: int
) -> list[dict]:
    """Compara a pessoa com todas as outras que têm ranking na categoria.

    Devolve ``[{"pessoa_id", "nome", "em_comum", "inversoes", "percentual"}, ...]``
    em ordem decrescente de percentual (empate: nome crescente).
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
                "em_comum": medida["em_comum"],
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
