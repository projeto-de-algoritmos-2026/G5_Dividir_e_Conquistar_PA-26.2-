"""Acesso ao banco: leitura e gravação de categorias, pessoas, rankings e notas.

Todas as funções recebem a conexão como primeiro parâmetro e devolvem tipos
simples (``dict``, ``list``, ``int``), nunca ``sqlite3.Row``.
"""

import sqlite3

NOTA_MINIMA = 0.0
NOTA_MAXIMA = 10.0


def listar_categorias(conn: sqlite3.Connection) -> list[dict]:
    """Devolve as categorias ordenadas por id."""
    linhas = conn.execute(
        "SELECT id, nome, eixo_x, eixo_y FROM categoria ORDER BY id"
    ).fetchall()
    return [dict(linha) for linha in linhas]


def listar_itens(conn: sqlite3.Connection, categoria_id: int) -> list[dict]:
    """Devolve os itens da categoria ordenados por id."""
    linhas = conn.execute(
        "SELECT id, nome FROM item WHERE categoria_id = ? ORDER BY id",
        (categoria_id,),
    ).fetchall()
    return [dict(linha) for linha in linhas]


def listar_pessoas(conn: sqlite3.Connection) -> list[dict]:
    """Devolve as pessoas cadastradas ordenadas por nome."""
    linhas = conn.execute("SELECT id, nome FROM pessoa ORDER BY nome").fetchall()
    return [dict(linha) for linha in linhas]


def criar_pessoa(conn: sqlite3.Connection, nome: str) -> int:
    """Cadastra uma pessoa e devolve o id gerado."""
    nome_limpo = nome.strip()
    if not nome_limpo:
        raise ValueError("O nome da pessoa não pode ser vazio.")

    try:
        with conn:
            cursor = conn.execute(
                "INSERT INTO pessoa (nome) VALUES (?)", (nome_limpo,)
            )
    except sqlite3.IntegrityError as erro:
        raise ValueError("Já existe uma pessoa com esse nome.") from erro

    return int(cursor.lastrowid)


def salvar_ranking(
    conn: sqlite3.Connection,
    pessoa_id: int,
    categoria_id: int,
    item_ids_em_ordem: list[int],
) -> None:
    """Grava o ranking da pessoa na categoria, substituindo o anterior.

    A lista tem só os itens de que a pessoa gosta (pelo menos 1), em ordem de
    preferência: ``item_ids_em_ordem[0]`` é o favorito (posição 1).
    """
    _exigir_pessoa(conn, pessoa_id)
    _exigir_categoria(conn, categoria_id)

    ids_da_categoria = [item["id"] for item in listar_itens(conn, categoria_id)]
    _validar_ranking(item_ids_em_ordem, ids_da_categoria)

    marcadores = ",".join("?" * len(ids_da_categoria))
    with conn:
        conn.execute(
            f"DELETE FROM ranking WHERE pessoa_id = ? AND item_id IN ({marcadores})",
            (pessoa_id, *ids_da_categoria),
        )
        conn.executemany(
            "INSERT INTO ranking (pessoa_id, item_id, posicao) VALUES (?, ?, ?)",
            [
                (pessoa_id, item_id, posicao)
                for posicao, item_id in enumerate(item_ids_em_ordem, start=1)
            ],
        )


def obter_ranking(
    conn: sqlite3.Connection, pessoa_id: int, categoria_id: int
) -> list[int]:
    """Devolve os item_id na ordem escolhida pela pessoa, ou [] se não houver."""
    linhas = conn.execute(
        """
        SELECT ranking.item_id
          FROM ranking
          JOIN item ON item.id = ranking.item_id
         WHERE ranking.pessoa_id = ? AND item.categoria_id = ?
         ORDER BY ranking.posicao
        """,
        (pessoa_id, categoria_id),
    ).fetchall()
    return [int(linha["item_id"]) for linha in linhas]


def pessoas_com_ranking(conn: sqlite3.Connection, categoria_id: int) -> list[dict]:
    """Devolve as pessoas que escolheram pelo menos 1 item na categoria."""
    linhas = conn.execute(
        """
        SELECT DISTINCT pessoa.id, pessoa.nome
          FROM pessoa
          JOIN ranking ON ranking.pessoa_id = pessoa.id
          JOIN item ON item.id = ranking.item_id AND item.categoria_id = ?
         ORDER BY pessoa.nome
        """,
        (categoria_id,),
    ).fetchall()
    return [dict(linha) for linha in linhas]


def salvar_nota(
    conn: sqlite3.Connection,
    pessoa_id: int,
    categoria_id: int,
    x: float,
    y: float,
) -> None:
    """Grava (ou atualiza) o ponto (x, y) da pessoa na categoria."""
    _validar_coordenada("x", x)
    _validar_coordenada("y", y)
    _exigir_pessoa(conn, pessoa_id)
    _exigir_categoria(conn, categoria_id)

    with conn:
        conn.execute(
            """
            INSERT INTO nota (pessoa_id, categoria_id, x, y) VALUES (?, ?, ?, ?)
            ON CONFLICT (pessoa_id, categoria_id)
            DO UPDATE SET x = excluded.x, y = excluded.y
            """,
            (pessoa_id, categoria_id, float(x), float(y)),
        )


def listar_notas(conn: sqlite3.Connection, categoria_id: int) -> list[dict]:
    """Devolve as notas da categoria ordenadas por pessoa_id."""
    linhas = conn.execute(
        """
        SELECT nota.pessoa_id, pessoa.nome, nota.x, nota.y
          FROM nota
          JOIN pessoa ON pessoa.id = nota.pessoa_id
         WHERE nota.categoria_id = ?
         ORDER BY nota.pessoa_id
        """,
        (categoria_id,),
    ).fetchall()
    return [
        {
            "pessoa_id": int(linha["pessoa_id"]),
            "nome": linha["nome"],
            "x": float(linha["x"]),
            "y": float(linha["y"]),
        }
        for linha in linhas
    ]


def _validar_ranking(item_ids_em_ordem: list[int], ids_da_categoria: list[int]) -> None:
    """Confere que o ranking tem pelo menos 1 item, sem repetição, todos da categoria."""
    if not item_ids_em_ordem:
        raise ValueError("Escolha pelo menos 1 item.")

    if len(set(item_ids_em_ordem)) != len(item_ids_em_ordem):
        raise ValueError("O ranking não pode repetir itens.")

    if set(item_ids_em_ordem) - set(ids_da_categoria):
        raise ValueError("O ranking contém item que não pertence à categoria.")


def _validar_coordenada(eixo: str, valor: float) -> None:
    """Confere que a coordenada está dentro de [0, 10]."""
    if not NOTA_MINIMA <= valor <= NOTA_MAXIMA:
        raise ValueError(f"A nota {eixo} deve estar entre 0 e 10.")


def _exigir_pessoa(conn: sqlite3.Connection, pessoa_id: int) -> None:
    """Levanta ValueError se a pessoa não existir."""
    if conn.execute("SELECT 1 FROM pessoa WHERE id = ?", (pessoa_id,)).fetchone() is None:
        raise ValueError("Pessoa não encontrada.")


def _exigir_categoria(conn: sqlite3.Connection, categoria_id: int) -> None:
    """Levanta ValueError se a categoria não existir."""
    existe = conn.execute(
        "SELECT 1 FROM categoria WHERE id = ?", (categoria_id,)
    ).fetchone()
    if existe is None:
        raise ValueError("Categoria não encontrada.")
