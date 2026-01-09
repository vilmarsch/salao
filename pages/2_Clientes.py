import streamlit as st
import psycopg2 as pg
import pandas as pd

# Conexão com Supabase (Postgres)
conn = pg.connect( st.secrets["SUPABASE_DB_URL"] )

st.title("👩‍🦱 Clientes")

# Cadastro de novo cliente
st.subheader("➕ Cadastrar novo cliente")
nome = st.text_input("Nome do cliente")
if st.button("Salvar") and nome:
    with conn.cursor() as cur:
        cur.execute( "INSERT INTO clientes (nome) VALUES (%s)", (nome,) )
        conn.commit()
    st.success("Cliente cadastrado")

# Edição / Exclusão de cliente
df = pd.read_sql( "SELECT * FROM clientes ORDER BY nome", conn )

st.subheader("✏️ Editar / Excluir cliente")

with st.form("form_editar_cliente"):
    cliente_id = st.selectbox( "Selecione o cliente", df["id"], format_func=lambda x: df.loc[df["id"] == x, "nome"].values[0] )
    nome_atual = df.loc[df["id"] == cliente_id, "nome"].values[0]
    novo_nome = st.text_input( "Nome do cliente", value=nome_atual )
    
    col1, col2 = st.columns(2)
    with col1:
        btn_atualizar = st.form_submit_button("💾 Atualizar")
    with col2:
        btn_excluir = st.form_submit_button("🗑️ Excluir")
        
    # Ações de atualizar ou excluir        
    if btn_atualizar:
        with conn.cursor() as cur:
            cur.execute( "UPDATE clientes SET nome=%s WHERE id=%s", (novo_nome, cliente_id) )
            conn.commit()
        st.success("Cliente atualizado")
    if btn_excluir:
        with conn.cursor() as cur:
            cur.execute( "DELETE FROM clientes WHERE id=%s", (cliente_id,) )
            conn.commit()
        st.success("Cliente excluído")

# Leitura dos dados e exibição
st.subheader("📋 Lista de clientes")
df = pd.read_sql( "SELECT * FROM clientes ORDER BY nome", conn )
st.dataframe(df, use_container_width=True)