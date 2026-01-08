import streamlit as st
import psycopg2
import pandas as pd

# -----------------------------
# Conexão com Supabase
# -----------------------------
@st.cache_resource
def get_conn():
    return psycopg2.connect(
        st.secrets["SUPABASE_DB_URL"]
    )

conn = get_conn()

st.title("✂️ Serviços")

# -----------------------------
# Cadastro
# -----------------------------
nome = st.text_input("Serviço")
preco = st.number_input("Preço", min_value=0.0, format="%.2f")

if st.button("Salvar serviço") and nome:
    with conn.cursor() as cur:
        cur.execute(
            """
            INSERT INTO servicos (nome, preco)
            VALUES (%s, %s)
            """,
            (nome, preco)
        )
        conn.commit()

    st.success("Serviço cadastrado")
    st.rerun()

# -----------------------------
# Listagem
# -----------------------------
df = pd.read_sql(
    "SELECT * FROM servicos ORDER BY nome",
    conn
)

st.dataframe(df, use_container_width=True)
