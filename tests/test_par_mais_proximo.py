"""Testes do par de pontos mais próximo."""

import math
import random

import pytest

from algoritmos.par_mais_proximo import par_mais_proximo

Ponto = tuple[float, float]


def par_forca_bruta(pontos: list[Ponto]) -> float:
    """Menor distância em O(n²), para servir de referência nos testes."""
    return min(
        math.dist(pontos[i], pontos[j])
        for i in range(len(pontos))
        for j in range(i + 1, len(pontos))
    )


def conferir_resposta(pontos: list[Ponto]) -> float:
    """Roda o algoritmo e confere o contrato do retorno. Devolve a distância."""
    original = list(pontos)

    distancia, i, j = par_mais_proximo(pontos)

    assert i < j
    assert 0 <= i < len(original) and 0 <= j < len(original)
    assert math.isclose(distancia, math.dist(original[i], original[j]))
    assert pontos == original, "a lista recebida não deve ser modificada"
    return distancia


@pytest.mark.parametrize("pontos", [[], [(1.0, 1.0)]])
def test_menos_de_dois_pontos(pontos: list[Ponto]) -> None:
    with pytest.raises(ValueError, match="pelo menos 2 pontos"):
        par_mais_proximo(pontos)


def test_dois_pontos() -> None:
    distancia, i, j = par_mais_proximo([(0.0, 0.0), (3.0, 4.0)])

    assert (i, j) == (0, 1)
    assert math.isclose(distancia, 5.0)


def test_pontos_repetidos_dao_distancia_zero() -> None:
    pontos: list[Ponto] = [(1.0, 1.0), (5.0, 5.0), (1.0, 1.0), (9.0, 2.0)]

    distancia, i, j = par_mais_proximo(pontos)

    assert math.isclose(distancia, 0.0)
    assert pontos[i] == pontos[j]


def test_varios_pontos_com_o_mesmo_x() -> None:
    pontos: list[Ponto] = [(5.0, 0.0), (5.0, 3.0), (5.0, 7.0), (5.0, 7.5), (5.0, 10.0)]

    assert math.isclose(conferir_resposta(pontos), 0.5)


def test_pontos_colineares() -> None:
    pontos: list[Ponto] = [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0), (2.5, 2.5), (4.0, 4.0)]

    assert math.isclose(conferir_resposta(pontos), math.dist((2.0, 2.0), (2.5, 2.5)))


def test_contra_forca_bruta_aleatorio() -> None:
    random.seed(42)

    for rodada in range(200):
        quantidade = random.randint(2, 80)
        if rodada % 2 == 0:
            # Coordenadas inteiras: força empates e muitos x iguais.
            pontos = [
                (float(random.randint(0, 10)), float(random.randint(0, 10)))
                for _ in range(quantidade)
            ]
        else:
            pontos = [
                (random.uniform(0, 10), random.uniform(0, 10))
                for _ in range(quantidade)
            ]

        distancia = conferir_resposta(pontos)

        assert math.isclose(distancia, par_forca_bruta(pontos))
