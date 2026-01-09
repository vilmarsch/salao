# app.py
import streamlit as st
import psycopg2 as pg
import pandas as pd

st.title("💇‍♀️Clau Hear")
st.write("Use o menu lateral para navegar")

# Mostrar abaixo a agenda de hoje
st.subheader("📅 Agenda de hoje")
conn = pg.connect( st.secrets["SUPABASE_DB_URL"] )
df = pd.read_sql( "SELECT \"data\", \"hora\", cliente, servico, valor FROM atendimentos ORDER BY \"data\", \"hora\" LIMIT 10;", conn )
df["data"] = pd.to_datetime(df["data"]).dt.strftime("%d/%m")
df["hora"] = pd.to_datetime(df["hora"], format="%H:%M:%S").dt.strftime("%H:%M")
df["valor"] = df["valor"].apply(lambda x: f"R$ {x:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
st.dataframe(df, use_container_width=True)