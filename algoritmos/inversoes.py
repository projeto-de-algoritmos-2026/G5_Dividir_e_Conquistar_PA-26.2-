"""Contagem de inversões por divisão e conquista (sort-and-count).

Referência: Kleinberg & Tardos, seção 5.3.
"""


def contar_inversoes(seq: list[int]) -> tuple[int, list[int]]:
    """Conta as inversões de ``seq`` e devolve ``(inversoes, seq ordenada)``.

    Uma inversão é um par de índices ``i < j`` com ``seq[i] > seq[j]``.
    Elementos iguais não contam como inversão. A lista recebida não é
    modificada.
    """
    return _ordenar_e_contar(list(seq))


def _ordenar_e_contar(seq: list[int]) -> tuple[int, list[int]]:
    """Divide a lista ao meio, resolve cada metade e intercala contando."""
    if len(seq) <= 1:
        return 0, seq

    meio = len(seq) // 2
    inv_esq, esq = _ordenar_e_contar(seq[:meio])
    inv_dir, dir_ = _ordenar_e_contar(seq[meio:])
    inv_cruzadas, intercalada = _intercalar_e_contar(esq, dir_)

    return inv_esq + inv_dir + inv_cruzadas, intercalada


def _intercalar_e_contar(esq: list[int], dir_: list[int]) -> tuple[int, list[int]]:
    """Intercala duas listas ordenadas contando as inversões entre elas."""
    inversoes = 0
    intercalada: list[int] = []
    i = j = 0

    while i < len(esq) and j < len(dir_):
        if esq[i] <= dir_[j]:
            # Empate não é inversão, por isso o <= aqui.
            intercalada.append(esq[i])
            i += 1
        else:
            # esq[i] > dir_[j]: todos os elementos restantes da esquerda
            # formam uma inversão com dir_[j].
            intercalada.append(dir_[j])
            j += 1
            inversoes += len(esq) - i

    intercalada.extend(esq[i:])
    intercalada.extend(dir_[j:])

    return inversoes, intercalada
