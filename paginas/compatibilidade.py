"""Aba Compatibilidade: compatibilidade entre rankings (contagem de inversões)."""

import sqlite3

import streamlit as st

from banco.repositorio import listar_categorias, pessoas_com_ranking
from servicos.compatibilidade import ranking_compatibilidade


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

    linhas = ranking_compatibilidade(conn, pessoa_id, categoria_id)
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
