import streamlit as st
from streamlit.components.v1 import html

st.title("Calendar")

calendar_code = """
<!DOCTYPE html>
<html>
  <head>
    <link href='https://cdn.jsdelivr.net/npm/fullcalendar@6.1.11/index.global.min.css' rel='stylesheet' />
    <script src='https://cdn.jsdelivr.net/npm/fullcalendar@6.1.11/index.global.min.js'></script>
    <style>
      #calendar {
        max-width: 900px;
        margin: 40px auto;
      }
    </style>
  </head>
  <body>
    <div id='calendar'></div>
    <script>
      document.addEventListener('DOMContentLoaded', function() {
        var calendarEl = document.getElementById('calendar');
        var calendar = new FullCalendar.Calendar(calendarEl, {
          initialView: 'dayGridMonth',
          headerToolbar: {
            left: 'prev,next today',
            center: 'title',
            right: 'dayGridMonth,timeGridWeek,timeGridDay,listWeek'
          },
          events: [
            { title: '就活', start: '2025-07-20' },
            { title: '遊び', start: '2025-07-22' },
            { title: '大学イベント', start: '2025-07-25' }
          ],
          dateClick: function(info) {
            alert('日付クリック: ' + info.dateStr);
          },
          eventClick: function(info) {
            alert('イベントクリック: ' + info.event.title);
          }
        });
        calendar.render();
      });
    </script>
  </body>
</html>
"""

html(calendar_code, height=800)
