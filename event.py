import streamlit as st
import streamlit_calendar as st_calendar


# イベントを定義
event1 = {
    'id': '1', # イベントを識別するためのID。重複不可
    'title': 'Data Cloud World Tour', # イベント名
    'start': '2025-07-08T09:00:00', # 時間帯も指定する
    'end': '2025-07-08T20:00:00', # 時間帯も指定する
}
event2 = {
    'id': '2',
    'title': '月〆',
    'start': '2025-07-31', # 日付のみ指定するとallDayがTrueになる。終日イベントとして表示される
}
event3 = {
    'id': '4',
    'editable': True, # ドラッグで開始日時や終了日時を変更できるようにする
    'groupId': 'Streamlit勉強会', # 同じgroupIdのイベントは同じ変更が適用される
    'title': 'Streamlit勉強会',
    'start': '2025-07-03T09:00:00',
    'end': '2025-07-03T11:00:00',
}
event4 = {
    'id': '4',
    'editable': True,
    'groupId': 'Streamlit勉強会',
    'title': 'Streamlit勉強会',
    'start': '2025-07-10T09:00:00',
    'end': '2025-07-10T11:00:00',
}
# calendarにはイベント一覧を配列にして渡す
event_list = [event1, event2, event3, event4]

# options = {
#     'initialView': 'timeGridWeek',
# }

# イベントを表示するカレンダーを作成
cal = st_calendar.calendar(events=event_list)
