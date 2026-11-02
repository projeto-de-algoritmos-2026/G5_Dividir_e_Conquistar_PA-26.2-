"""Aba Compatibilidade: compatibilidade entre rankings (contagem de inversões)."""

import sqlite3

import streamlit as st

from banco.repositorio import (
    listar_categorias,
    listar_itens,
    obter_ranking,
    pessoas_com_ranking,
)
from servicos.compatibilidade import compatibilidade, ranking_compatibilidade


def render(conn: sqlite3.Connection) -> None:
    """Desenha o conteúdo da aba."""
    categorias_por_id = {c["id"]: c for c in listar_categorias(conn)}
    categoria_id = st.selectbox(
        "Categoria",
        options=list(categorias_por_id),
        format_func=lambda cid: categorias_por_id[cid]["nome"],
        key="compatibilidade_categoria",
    )

    # Só entra quem tem ranking completo na categoria: sem ranking não há o que
    # comparar.
    nomes = {p["id"]: p["nome"] for p in pessoas_com_ranking(conn, categoria_id)}
    if len(nomes) < 2:
        st.info(
            "São necessárias pelo menos 2 pessoas com ranking nessa categoria. "
            "Salve os rankings na aba Cadastro."
        )
        return

    _secao_mais_compativeis(conn, categoria_id, nomes)
    st.divider()
    _secao_comparacao(conn, categoria_id, nomes)


def _secao_mais_compativeis(
    conn: sqlite3.Connection, categoria_id: int, nomes: dict[int, str]
) -> None:
    """Tabela com todas as outras pessoas, da mais para a menos compatível."""
    st.subheader("Mais compatíveis")

    # A chave inclui a categoria porque a lista de pessoas muda de uma
    # categoria para outra.
    pessoa_id = st.selectbox(
        "Pessoa",
        options=list(nomes),
        format_func=nomes.get,
        key=f"compatibilidade_pessoa_{categoria_id}",
    )

    try:
        linhas = ranking_compatibilidade(conn, pessoa_id, categoria_id)
    except ValueError as erro:
        st.error(str(erro))
        return

    st.dataframe(
        [
            {
                "Pessoa": linha["nome"],
                "Compatibilidade": linha["percentual"],
                "Inversões": linha["inversoes"],
            }
            for linha in linhas
        ],
        hide_index=True,
        column_config={
            "Compatibilidade": st.column_config.ProgressColumn(
                min_value=0, max_value=100, format="%.1f%%"
            ),
        },
    )


def _secao_comparacao(
    conn: sqlite3.Connection, categoria_id: int, nomes: dict[int, str]
) -> None:
    """Compatibilidade entre duas pessoas escolhidas."""
    st.subheader("Comparar duas pessoas")

    ids = list(nomes)
    col_a, col_b = st.columns(2)
    pessoa_a_id = col_a.selectbox(
        "Pessoa A",
        options=ids,
        format_func=nomes.get,
        key=f"compatibilidade_a_{categoria_id}",
    )
    pessoa_b_id = col_b.selectbox(
        "Pessoa B",
        options=ids,
        index=1,
        format_func=nomes.get,
        key=f"compatibilidade_b_{categoria_id}",
    )

    # Inclui o caso A == B: o backend devolve a mensagem pronta para mostrar.
    try:
        resultado = compatibilidade(conn, pessoa_a_id, pessoa_b_id, categoria_id)
    except ValueError as erro:
        st.error(str(erro))
        return

    col_percentual, col_inversoes = st.columns(2)
    col_percentual.metric("Compatibilidade", f"{resultado['percentual']:.1f}%")
    col_inversoes.metric(
        "Pares em desacordo (inversões)",
        f"{resultado['inversoes']} de {resultado['total_pares']}",
    )

    _rankings_lado_a_lado(conn, categoria_id, nomes, pessoa_a_id, pessoa_b_id)


def _rankings_lado_a_lado(
    conn: sqlite3.Connection,
    categoria_id: int,
    nomes: dict[int, str],
    pessoa_a_id: int,
    pessoa_b_id: int,
) -> None:
    """Os dois rankings, posição por posição, para ver onde eles discordam."""
    nomes_itens = {i["id"]: i["nome"] for i in listar_itens(conn, categoria_id)}
    ranking_a = obter_ranking(conn, pessoa_a_id, categoria_id)
    ranking_b = obter_ranking(conn, pessoa_b_id, categoria_id)

    st.dataframe(
        [
            {
                "Posição": posicao,
                nomes[pessoa_a_id]: nomes_itens[item_a],
                nomes[pessoa_b_id]: nomes_itens[item_b],
            }
            for posicao, (item_a, item_b) in enumerate(
                zip(ranking_a, ranking_b), start=1
            )
        ],
        hide_index=True,
    )
