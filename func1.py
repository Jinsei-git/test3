import streamlit as st
import datetime

@st.dialog("イベントの詳細を入力してください")
def vote(item):
    st.write(f"Why is {item} your favorite?")
    reason1 = st.text_input("イベント名", key="reason1")
    reason2 = st.date_input("日時", datetime.date(2025, 7, 9), key="reason2") 
    reason3 = st.text_input("場所", key="reason3")
    reason4 = st.selectbox("申し込み",("あり", "なし"),)
    if st.button("Submit"):
        st.session_state.vote = {"item": item, "reason1": reason1, "reason2": reason2, "reason3": reason3, "reason4": reason4}
        st.rerun()

if "vote" not in st.session_state:
    st.write("イベントの日時を選択してください")
    if st.button("07/07"):
        vote("07/07")
    if st.button("07/10"):
        vote("07/10")
else:
    st.write(f"{st.session_state.vote['reason1']}が、{st.session_state.vote['reason2']} に、{st.session_state.vote['reason3']}で開催されます。予約は {st.session_state.vote['reason4']}です。")
