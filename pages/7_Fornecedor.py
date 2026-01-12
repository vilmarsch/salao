import streamlit as st
import psycopg2 as pg
import pandas as pd

# Conexão com Supabase (Postgres)
conn = pg.connect( st.secrets["SUPABASE_DB_URL"] )

st.title("🚚 Fornecedor")

# Cadastro de novo fornecedor
st.subheader("➕ Cadastrar novo fornecedor")
nome = st.text_input("Nome do fornecedor")
telefone = st.text_input("Telefone")
email = st.text_input("Email")
if st.button("Salvar") and nome:
    with conn.cursor() as cur:
        cur.execute( "INSERT INTO fornecedores (nome, telefone, email) VALUES (%s, %s, %s)", (nome, telefone, email) )
        conn.commit()
    st.success("Fornecedor cadastrado")

# Edição / Exclusão de fornecedor
df = pd.read_sql( "SELECT * FROM fornecedores ORDER BY nome", conn )

st.subheader("✏️Excluir fornecedor")
fornecedor_id = st.selectbox( "Selecione o fornecedor", df["id"], format_func=lambda x: df.loc[df["id"] == x, "nome"].values[0] )
if st.button("Excluir") and fornecedor_id:
    with conn.cursor() as cur:
        cur.execute( "DELETE FROM fornecedores WHERE id=%s", (fornecedor_id,) )
        conn.commit()
    st.success("Fornecedor excluído")

# Leitura dos dados e exibição
st.subheader("📋 Lista de fornecedores")
df = pd.read_sql( "SELECT * FROM fornecedores ORDER BY nome", conn )
st.dataframe(df, use_container_width=True)