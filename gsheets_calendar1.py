import streamlit as st
from st-gsheets-connection import GSheetsConnection

conn = st.connection("gsheets", type=GSheetsConnection)
df = conn.read()

df
