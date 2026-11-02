"""Testes da contagem de inversões."""

import random

import pytest

from algoritmos.inversoes import contar_inversoes

CASOS = [
    ([], 0),
    ([1], 0),
    ([1, 2, 3, 4, 5], 0),
    ([5, 4, 3, 2, 1], 10),
    ([2, 4, 1, 3, 5], 3),
]


def inversoes_forca_bruta(seq: list[int]) -> int:
    """Conta inversões em O(n²), para servir de referência nos testes."""
    return sum(
        1
        for i in range(len(seq))
        for j in range(i + 1, len(seq))
        if seq[i] > seq[j]
    )


@pytest.mark.parametrize("seq, esperado", CASOS)
def test_casos_conhecidos(seq: list[int], esperado: int) -> None:
    original = list(seq)

    inversoes, ordenada = contar_inversoes(seq)

    assert inversoes == esperado
    assert ordenada == sorted(original)
    assert seq == original, "a lista recebida não deve ser modificada"


def test_elementos_repetidos_nao_contam_como_inversao() -> None:
    assert contar_inversoes([2, 2, 2]) == (0, [2, 2, 2])
    assert contar_inversoes([2, 1, 2]) == (1, [1, 2, 2])


def test_contra_forca_bruta_aleatorio() -> None:
    random.seed(42)

    for _ in range(200):
        tamanho = random.randint(0, 60)
        seq = list(range(tamanho))
        random.shuffle(seq)
        original = list(seq)

        inversoes, ordenada = contar_inversoes(seq)

        assert inversoes == inversoes_forca_bruta(original)
        assert ordenada == sorted(original)
        assert seq == original
