"""Par de pontos mais próximo por divisão e conquista.

Referência: Kleinberg & Tardos, seção 5.4 (equivalente a CLRS 33.4).
"""

import math

Ponto = tuple[float, float]


def par_mais_proximo(pontos: list[Ponto]) -> tuple[float, int, int]:
    """Devolve ``(menor distância, i, j)`` com ``i < j``.

    Os índices ``i`` e ``j`` se referem à lista original recebida, que não é
    modificada. Levanta ``ValueError`` se houver menos de 2 pontos.
    """
    if len(pontos) < 2:
        raise ValueError("São necessários pelo menos 2 pontos.")

    pts: list[Ponto] = [(float(x), float(y)) for x, y in pontos]

    # Pré-ordenação feita uma única vez: a recursão só reparticiona.
    por_x = sorted(range(len(pts)), key=lambda k: (pts[k][0], pts[k][1]))
    por_y = sorted(range(len(pts)), key=lambda k: (pts[k][1], pts[k][0]))

    return _resolver(pts, por_x, por_y)


def _resolver(
    pts: list[Ponto], por_x: list[int], por_y: list[int]
) -> tuple[float, int, int]:
    """Resolve o subproblema formado pelos índices em ``por_x``/``por_y``."""
    n = len(por_x)
    if n <= 3:
        return _forca_bruta(pts, por_x)

    meio = n // 2
    esq_x, dir_x = por_x[:meio], por_x[meio:]

    # A divisão da lista ordenada por y usa os ÍNDICES de cada metade, e não a
    # comparação de x: vários pontos podem ter o mesmo x e cair em metades
    # diferentes.
    da_esquerda = set(esq_x)
    esq_y = [k for k in por_y if k in da_esquerda]
    dir_y = [k for k in por_y if k not in da_esquerda]

    melhor = _resolver(pts, esq_x, esq_y)
    candidato = _resolver(pts, dir_x, dir_y)
    if candidato[0] < melhor[0]:
        melhor = candidato

    delta = melhor[0]
    x_linha = pts[dir_x[0]][0]

    # Faixa de largura 2*delta em torno da reta divisória, mantendo a ordem por y.
    faixa = [k for k in por_y if abs(pts[k][0] - x_linha) < delta]

    for a in range(len(faixa)):
        for b in range(a + 1, len(faixa)):
            # Só vale comparar com os próximos enquanto a diferença em y for
            # menor que delta. Para pontos distintos isso são no máximo 7
            # vizinhos; com pontos repetidos continua sendo uma constante.
            if pts[faixa[b]][1] - pts[faixa[a]][1] >= delta:
                break
            distancia = math.dist(pts[faixa[a]], pts[faixa[b]])
            if distancia < melhor[0]:
                i, j = sorted((faixa[a], faixa[b]))
                melhor = (distancia, i, j)

    return melhor


def _forca_bruta(pts: list[Ponto], indices: list[int]) -> tuple[float, int, int]:
    """Caso base: compara todos os pares (no máximo 3 pontos)."""
    melhor = (math.inf, -1, -1)
    for a in range(len(indices)):
        for b in range(a + 1, len(indices)):
            distancia = math.dist(pts[indices[a]], pts[indices[b]])
            if distancia < melhor[0]:
                i, j = sorted((indices[a], indices[b]))
                melhor = (distancia, i, j)
    return melhor
