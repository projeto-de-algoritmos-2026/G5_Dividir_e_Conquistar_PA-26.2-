"""Ponto de entrada do Ranking Match: `streamlit run app.py`."""

import streamlit as st

from banco.conexao import conectar
from paginas import cadastro, compatibilidade, dupla

st.set_page_config(page_title="Ranking Match", layout="wide")
st.title("Ranking Match")

# Conexão nova a cada rerun: o Streamlit roda cada rerun em outra thread e a
# conexão SQLite padrão só pode ser usada na thread que a criou.
conn = conectar()

aba_cadastro, aba_compatibilidade, aba_dupla = st.tabs(
    ["Cadastro", "Compatibilidade", "Dupla mais parecida"]
)

with aba_cadastro:
    cadastro.render(conn)

with aba_compatibilidade:
    compatibilidade.render(conn)

with aba_dupla:
    dupla.render(conn)
