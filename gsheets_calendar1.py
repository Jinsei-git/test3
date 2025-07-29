import streamlit as st
from streamlit_gsheets_connection import GSheetsConnection

conn = st.connection("gsheets", type=GSheetsConnection)
df = conn.read()

df
