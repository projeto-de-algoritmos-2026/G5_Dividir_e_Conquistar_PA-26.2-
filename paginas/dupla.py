"""Aba Dupla mais parecida: par de notas mais próximo da categoria."""

import sqlite3

import altair as alt
import streamlit as st

from banco.repositorio import listar_categorias, listar_notas

# Domínio um pouco maior que [0, 10] para os pontos nas bordas não ficarem
# cortados pela metade; as marcações do eixo continuam de 0 a 10.
DOMINIO = [-0.5, 10.5]
MARCACOES = list(range(11))


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

    notas = listar_notas(conn, categoria_id)
    st.altair_chart(_grafico(notas, categoria), width="stretch")


def _grafico(notas: list[dict], categoria: dict) -> alt.LayerChart:
    """Gráfico de dispersão das notas (x, y) da categoria."""
    eixo_x = alt.X(
        "x:Q",
        title=categoria["eixo_x"],
        scale=alt.Scale(domain=DOMINIO),
        axis=alt.Axis(values=MARCACOES),
    )
    eixo_y = alt.Y(
        "y:Q",
        title=categoria["eixo_y"],
        scale=alt.Scale(domain=DOMINIO),
        axis=alt.Axis(values=MARCACOES),
    )

    pontos = (
        alt.Chart(alt.Data(values=notas))
        .mark_circle(size=140, opacity=0.9)
        .encode(
            x=eixo_x,
            y=eixo_y,
            tooltip=[
                alt.Tooltip("nome:N", title="Pessoa"),
                alt.Tooltip("x:Q", title="x"),
                alt.Tooltip("y:Q", title="y"),
            ],
        )
    )

    nomes = pontos.mark_text(align="left", dx=9, dy=-9, fontSize=13).encode(
        text="nome:N"
    )

    return alt.layer(pontos, nomes).properties(height=480)
