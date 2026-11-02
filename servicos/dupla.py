"""Aba Dupla mais parecida: par de notas mais próximo de uma categoria."""

import sqlite3

from algoritmos.par_mais_proximo import par_mais_proximo
from banco.repositorio import listar_notas


def dupla_mais_parecida(conn: sqlite3.Connection, categoria_id: int) -> dict:
    """Devolve a dupla com as notas mais próximas na categoria.

    Formato: ``{"pessoa_a", "pessoa_b", "distancia"}``, em que ``pessoa_a`` é a
    de menor ``pessoa_id`` e cada pessoa é ``{"id", "nome", "x", "y"}``.
    """
    notas = listar_notas(conn, categoria_id)
    if len(notas) < 2:
        raise ValueError(
            "São necessárias pelo menos 2 pessoas com nota nessa categoria."
        )

    pontos = [(nota["x"], nota["y"]) for nota in notas]
    distancia, i, j = par_mais_proximo(pontos)

    primeira, segunda = notas[i], notas[j]
    if primeira["pessoa_id"] > segunda["pessoa_id"]:
        primeira, segunda = segunda, primeira

    return {
        "pessoa_a": _formatar(primeira),
        "pessoa_b": _formatar(segunda),
        "distancia": distancia,
    }


def _formatar(nota: dict) -> dict:
    """Converte uma linha de listar_notas no formato esperado pela interface."""
    return {
        "id": nota["pessoa_id"],
        "nome": nota["nome"],
        "x": nota["x"],
        "y": nota["y"],
    }
