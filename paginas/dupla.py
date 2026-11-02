"""Aba Dupla mais parecida: par de notas mais próximo da categoria."""

import sqlite3

import streamlit as st

from banco.repositorio import listar_categorias


def render(conn: sqlite3.Connection) -> None:
    """Desenha o conteúdo da aba."""
    categorias_por_id = {c["id"]: c for c in listar_categorias(conn)}
    categoria_id = st.selectbox(
        "Categoria",
        options=list(categorias_por_id),
        format_func=lambda cid: categorias_por_id[cid]["nome"],
        key="dupla_categoria",
    )
    categoria = categorias_por_id[categoria_id]
