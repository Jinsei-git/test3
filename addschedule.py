import streamlit as st
from streamlit.components.v1 import html
import json

st.title("📅 日付クリックでイベント追加カレンダー")

if "events" not in st.session_state:
    st.session_state.events = []

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
          selectable: true,
          headerToolbar: {{
            left: 'prev,next today',
            center: 'title',
            right: 'dayGridMonth,timeGridWeek,timeGridDay,listWeek'
          }},
          events: {json.dumps(st.session_state.events)},
          dateClick: function(info) {{
            var title = prompt('追加するイベント名を入力してください:');
            if (title) {{
              calendar.addEvent({{
                title: title,
                start: info.dateStr,
                allDay: true
              }});
            }}
          }},
          eventClick: function(info) {{
            if (confirm("このイベントを削除しますか？")) {{
              info.event.remove();
            }}
          }}
        }});
        calendar.render();
      }});
    </script>
  </body>
</html>
"""

html(calendar_code, height=800)
