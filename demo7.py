import streamlit as st
from streamlit.components.v1 import html
import json
import datetime

st.title("📅 共創カレンダー")

# 初期データ
if "events" not in st.session_state:
    st.session_state.events = [
        {"title": "就活", "start": "2025-07-20", "genre": "就活", "registration": "必要"},
        {"title": "遊び", "start": "2025-07-22", "genre": "遊び", "registration": "不要"},
        {"title": "大学イベント", "start": "2025-07-25", "genre": "大学イベント", "registration": "必要"}
    ]

GENRES = ["就活", "遊び", "大学イベント", "誕生日"]
COLOR_MAP = {"就活": "blue", "遊び": "green", "大学イベント": "orange", "誕生日": "purple"}

# サイドバー：フィルター
with st.sidebar:
    st.header("ジャンルフィルター")
    genre_filter = st.multiselect("ジャンルを選択", options=GENRES, default=GENRES)

    st.markdown("---")
    st.subheader("イベント追加")
    with st.form("add_event"):
        title = st.text_input("タイトル")
        date = st.date_input("日付", value=datetime.date.today())
        genre = st.selectbox("ジャンル", options=GENRES)
        registration = st.selectbox("事前申し込み", options=["必要", "不要"])
        submitted = st.form_submit_button("追加")

        if submitted and title:
            st.session_state.events.append({
                "title": title,
                "start": date.isoformat(),
                "genre": genre,
                "registration": registration
            })
            st.success("イベントを追加しました！")

# ✅ フィルターとカラー付与
filtered_events = []
for e in st.session_state.events:
    if e["genre"] in genre_filter:
        event_copy = e.copy()
        event_copy["color"] = COLOR_MAP.get(e["genre"], "gray")
        filtered_events.append(event_copy)

# ✅ FullCalendar 描画
calendar_code = f"""
<!DOCTYPE html>
<html>
  <head>
    <link href='https://cdn.jsdelivr.net/npm/fullcalendar@6.1.11/index.global.min.css' rel='stylesheet' />
    <script src='https://cdn.jsdelivr.net/npm/fullcalendar@6.1.11/index.global.min.js'></script>
    <style>
      #calendar {{
        max-width: 900px;
        margin: 40px auto;
      }}
    </style>
  </head>
  <body>
    <div id='calendar'></div>
    <script>
      document.addEventListener('DOMContentLoaded', function() {{
        var calendarEl = document.getElementById('calendar');
        var calendar = new FullCalendar.Calendar(calendarEl, {{
          initialView: 'dayGridMonth',
          headerToolbar: {{
            left: 'prev,next today',
            center: 'title',
            right: 'dayGridMonth,timeGridWeek,timeGridDay,listWeek'
          }},
          events: {json.dumps(filtered_events)},
          eventClick: function(info) {{
            var e = info.event.extendedProps;
            alert(
              'タイトル: ' + info.event.title + '\\n' +
              'ジャンル: ' + e.genre + '\\n' +
              '事前申し込み: ' + e.registration + '\\n' +
              '日付: ' + info.event.startStr
            );
          }}
        }});
        calendar.render();
      }});
    </script>
  </body>
</html>
"""

st.subheader("📆 カレンダー表示")
html(calendar_code, height=800)

# ✅ 編集・削除
st.subheader("📝 イベント一覧・編集・削除")

for idx, e in enumerate(st.session_state.events):
    with st.expander(f"{e['title']} ({e['start']})"):
        new_title = st.text_input(f"タイトル (index {idx})", e['title'], key=f"title_{idx}")
        new_date = st.date_input(f"日付 (index {idx})", datetime.date.fromisoformat(e['start']), key=f"date_{idx}")
        new_genre = st.selectbox(f"ジャンル (index {idx})", GENRES, index=GENRES.index(e['genre']), key=f"genre_{idx}")
        new_registration = st.selectbox(f"事前申し込み (index {idx})", ["必要", "不要"], index=["必要", "不要"].index(e['registration']), key=f"reg_{idx}")

        if st.button("更新", key=f"update_{idx}"):
            st.session_state.events[idx] = {
                "title": new_title,
                "start": new_date.isoformat(),
                "genre": new_genre,
                "registration": new_registration
            }
            st.success(f"{new_title} を更新しました。")

        if st.button("削除", key=f"delete_{idx}"):
            st.session_state.events.pop(idx)
            st.success(f"{e['title']} を削除しました。")
            st.rerun()
