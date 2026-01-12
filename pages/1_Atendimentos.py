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
servicos = pd.read_sql("SELECT id, nome, preco FROM servicos ORDER BY nome", conn)  

st.title("📅 Atendimentos")

# -----------------------------
# Novo atendimento
# -----------------------------
with st.form("novo_atendimento"):
    data = st.date_input("Data", date.today(), format="DD/MM/YYYY")
    hora = st.time_input("Hora", value=None)
    cliente = st.selectbox("Cliente", clientes)
    servico = st.multiselect("Serviço", servicos['nome'])

    qtd = len(servico)
    if qtd == 2:
        desconto = 0.10
    elif qtd >= 3:
        desconto = 0.15
    else:
        desconto = 0
    valor = sum(float(servicos.loc[servicos['nome'] == s, 'preco'].values[0]) for s in servico) * (1 - desconto)

    pagamento = st.selectbox("Forma de pagamento", ["Dinheiro", "PIX", "Cartão"])
    
    salvar = st.form_submit_button("Salvar")

    if salvar:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO atendimentos
                (data, hora, cliente, valor, pagamento, desconto)
                VALUES (%s, %s, %s, %s, %s, %s)
                RETURNING id
            """, (data, hora, cliente, valor, pagamento, desconto))

            atendimento_id = cur.fetchone()[0]

            map_servico = dict(zip(servicos['nome'], servicos['id']))
            for nome_servico in servico:
                servico_id = map_servico[nome_servico]
                preco = float(
                    servicos.loc[servicos['id'] == servico_id, 'preco'].iloc[0]
                )

                cur.execute("""
                    INSERT INTO atendimento_servicos
                    (atendimento_id, servico_id, valor)
                    VALUES (%s, %s, %s)
                """, (atendimento_id, servico_id, preco))
            conn.commit()

        st.success("Atendimento salvo")
        st.rerun()

st.divider()

# -----------------------------
# Excluir atendimento
# -----------------------------
st.subheader("Excluir de Atendimentos")

df = pd.read_sql("SELECT * FROM atendimentos ORDER BY data DESC",conn)

if df.empty:
    st.info("Nenhum atendimento cadastrado")
else:
    selected_id = st.selectbox("Selecione um atendimento para excluir",df['id'])

    registro = df[df['id'] == selected_id].iloc[0]

excluir = st.button("Excluir")
if excluir:
    with conn.cursor() as cur:
        cur.execute("DELETE FROM atendimentos WHERE id=%s",(selected_id,))
        conn.commit()

    st.warning("Atendimento excluído")
    st.rerun()

st.divider()
# -----------------------------
# Ver atendimentos
# -----------------------------
st.subheader("Ver Atendimentos")
df = pd.read_sql("SELECT id, data, hora, cliente, valor, pagamento, desconto FROM atendimentos ORDER BY data DESC, hora DESC",conn)
df["data"] = pd.to_datetime(df["data"]).dt.strftime("%d/%m/%Y")
df["hora"] = pd.to_datetime(df["hora"], format="%H:%M:%S").dt.strftime("%H:%M")
df["valor"] = df["valor"].apply(lambda x: f"R$ {x:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
st.dataframe(df, hide_index=True)