"""Aba Cadastro: criar pessoa e salvar ranking e notas."""

import sqlite3
import unicodedata

import streamlit as st

from banco.repositorio import (
    criar_pessoa,
    listar_categorias,
    listar_itens,
    listar_notas,
    listar_pessoas,
    obter_ranking,
    salvar_nota,
    salvar_ranking,
)

# Chave do selectbox de pessoa. Fica numa constante porque o formulário de
# nova pessoa escreve nela para já deixar a pessoa recém-criada selecionada.
CHAVE_PESSOA = "cadastro_pessoa"


def render(conn: sqlite3.Connection) -> None:
    """Desenha o conteúdo da aba."""
    _secao_nova_pessoa(conn)
    st.divider()

    pessoas = listar_pessoas(conn)
    categorias = listar_categorias(conn)
    nomes_pessoas = {p["id"]: p["nome"] for p in pessoas}
    categorias_por_id = {c["id"]: c for c in categorias}

    col_pessoa, col_categoria = st.columns(2)
    pessoa_id = col_pessoa.selectbox(
        "Pessoa",
        options=list(nomes_pessoas),
        format_func=nomes_pessoas.get,
        key=CHAVE_PESSOA,
    )
    categoria_id = col_categoria.selectbox(
        "Categoria",
        options=list(categorias_por_id),
        format_func=lambda cid: categorias_por_id[cid]["nome"],
        key="cadastro_categoria",
    )

    # Com ~50 itens por categoria, a escolha ocupa a largura toda e as notas
    # ficam logo abaixo.
    _secao_ranking(conn, pessoa_id, categoria_id)
    st.divider()
    _secao_notas(conn, pessoa_id, categorias_por_id[categoria_id])


def _secao_nova_pessoa(conn: sqlite3.Connection) -> None:
    """Formulário para cadastrar uma pessoa nova."""
    st.subheader("Nova pessoa")
    with st.form("cadastro_nova_pessoa", clear_on_submit=True):
        nome = st.text_input("Nome")
        enviado = st.form_submit_button("Cadastrar")

    if not enviado:
        return

    try:
        novo_id = criar_pessoa(conn, nome)
    except ValueError as erro:
        st.error(str(erro))
        return

    # O selectbox de pessoa ainda não foi desenhado nesta execução, então dá
    # para definir o valor dele aqui.
    st.session_state[CHAVE_PESSOA] = novo_id
    st.success(f"Pessoa cadastrada: {nome.strip()}. Agora escolha do que gosta e as notas.")


def _secao_ranking(conn: sqlite3.Connection, pessoa_id: int, categoria_id: int) -> None:
    """Lista de itens da categoria: a pessoa clica nos que gosta.

    A ordem dos cliques vira a ordem de preferência (1º clicado = favorito),
    que é o que a aba Compatibilidade usa para contar inversões.
    """
    st.subheader("Do que você gosta")
    st.caption(
        "Clique nos itens de que você gosta, começando pelos que mais gosta. "
        "Clique de novo para tirar da lista."
    )

    itens = listar_itens(conn, categoria_id)
    nomes_itens = {i["id"]: i["nome"] for i in itens}
    salvo = obter_ranking(conn, pessoa_id, categoria_id)

    # Uma lista por pessoa e categoria, começando pelo que já está salvo.
    chave = f"cadastro_lista_{pessoa_id}_{categoria_id}"
    if chave not in st.session_state:
        st.session_state[chave] = salvo
    escolhidos: list[int] = st.session_state[chave]

    col_itens, col_lista = st.columns([3, 1], gap="large")

    with col_itens:
        busca = st.text_input(
            "Buscar",
            placeholder="Digite parte do nome",
            key=f"cadastro_busca_{categoria_id}",
        )
        _grade_de_itens(itens, escolhidos, busca, chave, pessoa_id, categoria_id)

    with col_lista:
        _sua_lista(conn, pessoa_id, categoria_id, nomes_itens, escolhidos, salvo, chave)


def _sem_acento(texto: str) -> str:
    """Minúsculas e sem acentos, para a busca achar "porao" em "Porão"."""
    decomposto = unicodedata.normalize("NFD", texto.casefold())
    return "".join(c for c in decomposto if unicodedata.category(c) != "Mn")


def _grade_de_itens(
    itens: list[dict],
    escolhidos: list[int],
    busca: str,
    chave: str,
    pessoa_id: int,
    categoria_id: int,
) -> None:
    """Botões dos itens em ordem alfabética, filtrados pela busca."""
    termo = _sem_acento(busca.strip())
    visiveis = sorted(
        (i for i in itens if termo in _sem_acento(i["nome"])),
        key=lambda i: _sem_acento(i["nome"]),
    )
    if not visiveis:
        st.caption("Nenhum item encontrado.")
        return

    # Preenche coluna por coluna, para a ordem alfabética ser lida de cima
    # para baixo.
    por_coluna = -(-len(visiveis) // 3)
    colunas = st.columns(3)
    for indice, item in enumerate(visiveis):
        selecionado = item["id"] in escolhidos
        rotulo = (
            f"{escolhidos.index(item['id']) + 1}. {item['nome']}"
            if selecionado
            else item["nome"]
        )
        colunas[indice // por_coluna].button(
            rotulo,
            key=f"cadastro_item_{pessoa_id}_{categoria_id}_{item['id']}",
            type="primary" if selecionado else "secondary",
            width="stretch",
            on_click=_alternar_item,
            args=(chave, item["id"]),
        )


def _sua_lista(
    conn: sqlite3.Connection,
    pessoa_id: int,
    categoria_id: int,
    nomes_itens: dict[int, str],
    escolhidos: list[int],
    salvo: list[int],
    chave: str,
) -> None:
    """Lista numerada do que a pessoa escolheu, com os botões de salvar e limpar."""
    st.markdown("**Sua lista**")
    if escolhidos:
        st.markdown(
            "\n".join(
                f"{posicao}. {nomes_itens[item_id]}"
                for posicao, item_id in enumerate(escolhidos, start=1)
            )
        )
    else:
        st.caption("Nenhum item escolhido ainda.")

    col_salvar, col_limpar = st.columns(2)
    salvar = col_salvar.button(
        "Salvar lista",
        disabled=not escolhidos,
        key=f"cadastro_salvar_ranking_{pessoa_id}_{categoria_id}",
    )
    col_limpar.button(
        "Limpar",
        disabled=not escolhidos,
        key=f"cadastro_limpar_{pessoa_id}_{categoria_id}",
        on_click=_limpar_lista,
        args=(chave,),
    )

    if salvar:
        try:
            salvar_ranking(conn, pessoa_id, categoria_id, escolhidos)
        except ValueError as erro:
            st.error(str(erro))
        else:
            salvo = escolhidos
            st.success("Lista salva.")

    if escolhidos and escolhidos != salvo:
        st.caption("Alterações não salvas.")


def _alternar_item(chave: str, item_id: int) -> None:
    """Põe o item no fim da lista ou, se já estiver nela, tira."""
    lista = st.session_state[chave]
    if item_id in lista:
        st.session_state[chave] = [i for i in lista if i != item_id]
    else:
        st.session_state[chave] = [*lista, item_id]


def _limpar_lista(chave: str) -> None:
    """Esvazia a lista (o que está salvo no banco só muda ao salvar)."""
    st.session_state[chave] = []


def _secao_notas(conn: sqlite3.Connection, pessoa_id: int, categoria: dict) -> None:
    """Ponto (x, y) da pessoa na categoria."""
    st.subheader("Notas")
    st.caption("0 = lado esquerdo do eixo, 10 = lado direito.")

    categoria_id = categoria["id"]
    nota_atual = next(
        (n for n in listar_notas(conn, categoria_id) if n["pessoa_id"] == pessoa_id),
        None,
    )
    x_inicial = nota_atual["x"] if nota_atual else 5.0
    y_inicial = nota_atual["y"] if nota_atual else 5.0

    sufixo = f"{pessoa_id}_{categoria_id}"
    x = st.slider(
        categoria["eixo_x"], 0.0, 10.0, x_inicial, step=0.5, key=f"cadastro_x_{sufixo}"
    )
    y = st.slider(
        categoria["eixo_y"], 0.0, 10.0, y_inicial, step=0.5, key=f"cadastro_y_{sufixo}"
    )

    if st.button("Salvar notas", key=f"cadastro_salvar_notas_{sufixo}"):
        try:
            salvar_nota(conn, pessoa_id, categoria_id, x, y)
        except ValueError as erro:
            st.error(str(erro))
        else:
            st.success("Notas salvas.")
