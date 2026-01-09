# app.py
import streamlit as st
import psycopg2 as pg
import pandas as pd

st.title("💇‍♀️Clau Hear")
st.write("Use o menu lateral para navegar")

# Mostrar abaixo a agenda de hoje
st.subheader("📅 Agenda de hoje")
conn = pg.connect( st.secrets["SUPABASE_DB_URL"] )
df = pd.read_sql( "SELECT \"data\", \"hora\", cliente, servico FROM atendimentos ORDER BY \"data\", \"hora\" LIMIT 10;", conn )
st.dataframe(df, use_container_width=True)