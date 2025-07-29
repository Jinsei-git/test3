import streamlit as st
from st_gsheets_connection import GSheetsConnection

conn = st.connection("gsheets", type=GSheetsConnection)
df = conn.read()

df
