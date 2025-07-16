import streamlit as st
from datetime import datetime, date, time, timedelta

st.title("Streamlit Datetime Showcase")

st.header("1️. 日付選択")
selected_date = st.date_input(
    "日付を選んでください",
    value=date.today(),
    min_value=date(2000, 1, 1),
    max_value=date(2100, 12, 31)
)
st.write("選んだ日付:", selected_date)

st.header("2️. 日付範囲選択")
date_range = st.date_input(
    "日付の範囲を選んでください",
    value=(date.today(), date.today() + timedelta(days=7))
)
if isinstance(date_range, tuple):
    st.write("開始日:", date_range[0])
    st.write("終了日:", date_range[1])

st.header("3️. 時刻選択")
selected_time = st.time_input(
    "時間を選んでください",
    value=time(12, 0)
)
st.write("選んだ時間:", selected_time)

st.header("4️. 日時選択")
datetime_date = st.date_input("日時選択 - 日付部分", value=date.today())
datetime_time = st.time_input("日時選択 - 時間部分", value=datetime.now().time())

combined_datetime = datetime.combine(datetime_date, datetime_time)
st.write("選んだ日時:", combined_datetime)

st.header("5️. 現在時刻・日付ボタン")
if st.button("現在の日時を取得"):
    now = datetime.now()
    st.write("🕒 現在の日時:", now)

st.header("6️. 時間間隔の選択")
hour = st.slider("時間（0〜23）", 0, 23, 12)
minute = st.slider("分（0〜59）", 0, 59, 0)
second = st.slider("秒（0〜59）", 0, 59, 0)

time_interval = time(hour, minute, second)
st.write("選んだ時間:", time_interval)
