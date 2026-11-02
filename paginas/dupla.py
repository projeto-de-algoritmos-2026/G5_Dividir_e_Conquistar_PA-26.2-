"""Aba Dupla mais parecida: par de notas mais próximo da categoria."""

import sqlite3

import altair as alt
import streamlit as st

from banco.repositorio import listar_categorias, listar_notas
from servicos.dupla import dupla_mais_parecida

# Domínio um pouco maior que [0, 10] para os pontos nas bordas não ficarem
# cortados pela metade; as marcações do eixo continuam de 0 a 10.
DOMINIO = [-0.5, 10.5]
MARCACOES = list(range(11))

GRUPO_DUPLA = "Dupla mais parecida"
GRUPO_DEMAIS = "Demais pessoas"
COR_DUPLA = "#ff4b4b"
COR_DEMAIS = "#8c8c8c"


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
    try:
        dupla = dupla_mais_parecida(conn, categoria_id)
    except ValueError as erro:
        # Menos de 2 pessoas com nota: mostra o que houver, sem destaque.
        st.altair_chart(_grafico(notas, set(), categoria), width="stretch")
        st.error(str(erro))
        return

    ids_dupla = {dupla["pessoa_a"]["id"], dupla["pessoa_b"]["id"]}
    st.altair_chart(_grafico(notas, ids_dupla, categoria), width="stretch")

    pessoa_a, pessoa_b = dupla["pessoa_a"], dupla["pessoa_b"]
    col_dupla, col_distancia = st.columns(2)
    col_dupla.metric("Dupla mais parecida", f"{pessoa_a['nome']} e {pessoa_b['nome']}")
    col_distancia.metric("Distância", f"{dupla['distancia']:.2f}")
    st.caption(
        f"{pessoa_a['nome']}: ({pessoa_a['x']:g}, {pessoa_a['y']:g}) · "
        f"{pessoa_b['nome']}: ({pessoa_b['x']:g}, {pessoa_b['y']:g}). "
        "Par de pontos mais próximo, encontrado por divisão e conquista."
    )


def _grafico(notas: list[dict], ids_dupla: set[int], categoria: dict) -> alt.LayerChart:
    """Gráfico de dispersão das notas, com a dupla destacada e ligada por uma linha."""
    for nota in notas:
        nota["grupo"] = GRUPO_DUPLA if nota["pessoa_id"] in ids_dupla else GRUPO_DEMAIS

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

    cor = alt.Color(
        "grupo:N",
        title=None,
        scale=alt.Scale(
            domain=[GRUPO_DUPLA, GRUPO_DEMAIS], range=[COR_DUPLA, COR_DEMAIS]
        ),
        legend=alt.Legend(orient="top"),
    )

    # Linha tracejada entre os dois pontos da dupla, desenhada por baixo deles.
    linha = (
        alt.Chart(alt.Data(values=[n for n in notas if n["grupo"] == GRUPO_DUPLA]))
        .mark_line(color=COR_DUPLA, strokeDash=[6, 4], strokeWidth=2)
        .encode(x=eixo_x, y=eixo_y)
    )

    pontos = (
        alt.Chart(alt.Data(values=notas))
        .mark_circle(size=140, opacity=0.9)
        .encode(
            x=eixo_x,
            y=eixo_y,
            color=cor,
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

    return alt.layer(linha, pontos, nomes).properties(height=480)
