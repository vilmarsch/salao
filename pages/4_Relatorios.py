import streamlit as st
import pandas as pd
import psycopg2

# -----------------------------
# Conexão com Supabase
# -----------------------------
@st.cache_resource
def get_conn():
    return psycopg2.connect(
        st.secrets["SUPABASE_DB_URL"]
    )

conn = get_conn()

# -----------------------------
# Leitura dos dados
# -----------------------------
df = pd.read_sql(
    "SELECT * FROM atendimentos",
    conn
)

if df.empty:
    st.warning("Sem dados ainda")
    st.stop()

# -----------------------------
# Tratamentos
# -----------------------------
df['data'] = pd.to_datetime(df['data'])
df['mes'] = df['data'].dt.to_period('M').astype(str)

st.title("📊 Relatórios")

# -----------------------------
# Indicadores
# -----------------------------
col1, col2, col3 = st.columns(3)

col1.metric("Atendimentos", len(df))
col2.metric("Faturamento", f"R$ {df['valor'].sum():,.2f}")
col3.metric("Ticket Médio", f"R$ {df['valor'].mean():,.2f}")

# -----------------------------
# Filtros
# -----------------------------
st.subheader("Filtros")

mes = st.selectbox(
    "Mês",
    sorted(df['mes'].unique())
)

df_filtrado = df[df['mes'] == mes]

# -----------------------------
# Gráficos
# -----------------------------
st.subheader("Atendimentos por forma de pagamento")

st.bar_chart(
    df_filtrado.groupby('pagamento')['valor'].sum()
)

# -----------------------------
# Exportação
# -----------------------------
st.subheader("Exportar dados")

st.download_button(
    "Baixar CSV",
    df_filtrado.to_csv(index=False),
    "relatorio.csv"
)