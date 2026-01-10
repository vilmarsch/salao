import streamlit as st
import pandas as pd
import psycopg2
from datetime import date

# -----------------------------
# Conexão com Supabase
# -----------------------------
@st.cache_resource
def get_conn():
    return psycopg2.connect( st.secrets["SUPABASE_DB_URL"] )
conn = get_conn()

# -----------------------------
# Dados auxiliares
# -----------------------------
clientes = pd.read_sql( "SELECT nome FROM clientes ORDER BY nome", conn )['nome'].tolist()
servicos = pd.read_sql( "SELECT nome, preco FROM servicos ORDER BY nome", conn )

st.title("📅 Atendimentos")

# -----------------------------
# Novo atendimento
# -----------------------------
with st.form("novo_atendimento"):
    data = st.date_input("Data", date.today(), format="DD/MM/YYYY")
    hora = st.time_input("Hora", value=None)
    cliente = st.selectbox("Cliente", clientes)
    servico = st.multiselect("Serviço", servicos['nome'])
    valor = sum(float(servicos.loc[servicos['nome'] == s, 'preco'].values[0]) for s in servico)
    pagamento = st.selectbox("Forma de pagamento", ["Dinheiro", "PIX", "Cartão"])
    
    salvar = st.form_submit_button("Salvar")
    if salvar:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO atendimentos
                (data, hora, cliente, servico, valor, pagamento)
                VALUES (%s, %s, %s, %s, %s, %s)
                """,
                (data, hora, cliente, servico, valor, pagamento)
            )
            conn.commit()

        st.success("Atendimento salvo")
        st.rerun()

st.divider()

# -----------------------------
# Histórico
# -----------------------------
st.subheader("Histórico de Atendimentos")

df = pd.read_sql("SELECT * FROM atendimentos ORDER BY data DESC",conn)

if df.empty:
    st.info("Nenhum atendimento cadastrado")
else:
    selected_id = st.selectbox("Selecione um atendimento para editar/excluir",df['id'])

    registro = df[df['id'] == selected_id].iloc[0]

    with st.form("editar_atendimento"):
        data_e = st.date_input("Data",pd.to_datetime(registro['data']).date())
        hora_e = st.text_input("Hora",registro['hora'])
        cliente_e = st.selectbox("Cliente",clientes,index=clientes.index(registro['cliente']))
        servico_e = st.multiselect("Serviço",servicos['nome'],default=servicos['nome'].tolist())
        valor_e = sum(float(servicos.loc[servicos['nome'] == s, 'preco'].values[0]) for s in servico_e)
        pagamento_e = st.selectbox("Pagamento",["Dinheiro", "PIX", "Cartão"],
            index=["Dinheiro", "PIX", "Cartão"].index(registro['pagamento']))

        col1, col2 = st.columns(2)
        atualizar = col1.form_submit_button("Atualizar")
        excluir = col2.form_submit_button("Excluir")

        if atualizar:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    UPDATE atendimentos
                    SET data=%s, hora=%s, cliente=%s, servico=%s, valor=%s, pagamento=%s
                    WHERE id=%s
                    """,
                    (data_e, hora_e, cliente_e, servico_e, valor_e, pagamento_e, selected_id)
                )
                conn.commit()

            st.success("Atendimento atualizado")
            st.rerun()

        if excluir:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM atendimentos WHERE id=%s",(selected_id,))
                conn.commit()

            st.warning("Atendimento excluído")
            st.rerun()