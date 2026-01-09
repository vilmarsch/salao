import streamlit as st
import psycopg2
import pandas as pd

# -----------------------------
# Conexão com Supabase
# -----------------------------
@st.cache_resource
def get_conn():
    return psycopg2.connect( st.secrets["SUPABASE_DB_URL"] )

conn = get_conn()

st.title("✂️ Serviços")

# -----------------------------
# Cadastro
# -----------------------------
nome = st.text_input("Serviço")
preco = st.number_input("Preço", min_value=0.0, format="%.2f")

if st.button("Salvar serviço") and nome:
    with conn.cursor() as cur:
        cur.execute( """INSERT INTO servicos (nome, preco) VALUES (%s, %s)""",(nome, preco))
        conn.commit()

    st.success("Serviço cadastrado")
    st.rerun()

# -----------------------------
# Edição / Exclusão de serviço
# -----------------------------
df = pd.read_sql( "SELECT * FROM servicos ORDER BY nome", conn )

st.subheader("✏️ Editar / Excluir serviço")

with st.form("form_editar_servico"):
    servico_id = st.selectbox( "Selecione o serviço", df["id"], format_func=lambda x: df.loc[df["id"] == x, "nome"].values[0] )
    nome_atual = df.loc[df["id"] == servico_id, "nome"].values[0]
    novo_nome = st.text_input( "Nome do serviço", value=nome_atual )
    novo_preco = st.number_input( "Preço do serviço", value=df.loc[df["id"] == servico_id, "preco"].values[0] )

    col1, col2 = st.columns(2)
    with col1:
        btn_atualizar = st.form_submit_button("💾 Atualizar")
    with col2:
        btn_excluir = st.form_submit_button("🗑️ Excluir")
        
    # Ações de atualizar ou excluir        
    if btn_atualizar:
        with conn.cursor() as cur:
            cur.execute( "UPDATE servicos SET nome=%s, preco=%s WHERE id=%s", (novo_nome, novo_preco, servico_id) )
            conn.commit()
        st.success("Serviço atualizado")
    if btn_excluir:
        with conn.cursor() as cur:
            cur.execute( "DELETE FROM servicos WHERE id=%s", (servico_id,) )
            conn.commit()
        st.success("Serviço excluído")

# -----------------------------
# Listagem
# -----------------------------
df = pd.read_sql("SELECT * FROM servicos ORDER BY nome", conn)
st.dataframe(df, use_container_width=True)
