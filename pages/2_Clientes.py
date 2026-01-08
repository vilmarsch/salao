import streamlit as st
import psycopg2
import pandas as pd

# Conexão com Supabase (Postgres)
conn = psycopg2.connect(
    st.secrets["SUPABASE_DB_URL"]
)

st.title("👩‍🦱 Clientes")

nome = st.text_input("Nome do cliente")

if st.button("Salvar cliente") and nome:
    with conn.cursor() as cur:
        cur.execute(
            "INSERT INTO clientes (nome) VALUES (%s)",
            (nome,)
        )
        conn.commit()
    st.success("Cliente cadastrado")

# Leitura dos dados
df = pd.read_sql(
    "SELECT * FROM clientes ORDER BY nome",
    conn
)

st.dataframe(df, use_container_width=True)
