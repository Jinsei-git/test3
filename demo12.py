import streamlit as st
from streamlit.components.v1 import html
import json
import datetime
import pandas as pd
import io

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

# --- サイドバー ---
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
            st.rerun()

    st.markdown("---")
    st.subheader("📂 イベントのCSV保存/読み込み")

    # --- CSV保存（ダウンロード） ---
    if st.session_state.events:
        df_all = pd.DataFrame(st.session_state.events)
        df_all = df_all.rename(columns={
            "start": "日付",
            "title": "タイトル",
            "genre": "ジャンル",
            "registration": "事前申し込み"
        })
        
        # UTF-8 with BOM for Excel compatibility
        csv_buffer = io.StringIO()
        df_all.to_csv(csv_buffer, index=False, encoding="utf-8-sig")
        csv_data = csv_buffer.getvalue()
        
        st.download_button(
            label="📥 CSVをダウンロード",
            data=csv_data.encode("utf-8-sig"),
            file_name=f"events_{datetime.date.today().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )

    # --- CSVアップロード ---
    uploaded_file = st.file_uploader("📤 CSVを読み込む", type=['csv'])
    if uploaded_file:
        try:
            # 複数のエンコーディングを試行
            try:
                df = pd.read_csv(uploaded_file, encoding="utf-8-sig")
            except UnicodeDecodeError:
                try:
                    uploaded_file.seek(0)  # ファイルポインタを先頭に戻す
                    df = pd.read_csv(uploaded_file, encoding="cp932")
                except UnicodeDecodeError:
                    uploaded_file.seek(0)
                    df = pd.read_csv(uploaded_file, encoding="utf-8")
            
            # 必要なカラムの確認
            required_columns = {'日付', 'タイトル', 'ジャンル', '事前申し込み'}
            if required_columns.issubset(df.columns):
                # データの検証とクリーニング
                valid_events = []
                for _, row in df.iterrows():
                    try:
                        # 日付の検証
                        date_str = str(row['日付'])
                        if date_str and date_str != 'nan':
                            # 様々な日付形式に対応
                            try:
                                datetime.datetime.fromisoformat(date_str)
                                start_date = date_str
                            except ValueError:
                                try:
                                    parsed_date = pd.to_datetime(date_str)
                                    start_date = parsed_date.strftime('%Y-%m-%d')
                                except:
                                    continue  # 無効な日付はスキップ
                            
                            # ジャンルの検証
                            genre = str(row['ジャンル'])
                            if genre not in GENRES:
                                genre = GENRES[0]  # デフォルトジャンル
                            
                            # 事前申し込みの検証
                            registration = str(row['事前申し込み'])
                            if registration not in ["必要", "不要"]:
                                registration = "不要"  # デフォルト値
                            
                            valid_events.append({
                                "start": start_date,
                                "title": str(row['タイトル']) if str(row['タイトル']) != 'nan' else "無題",
                                "genre": genre,
                                "registration": registration
                            })
                    except Exception as e:
                        st.warning(f"行のスキップ: {e}")
                        continue
                
                if valid_events:
                    st.session_state.events = valid_events
                    st.success(f"CSVから{len(valid_events)}件のイベントを読み込みました。")
                    st.rerun()
                else:
                    st.error("有効なイベントデータが見つかりませんでした。")
            else:
                st.error(f"CSVに必要なカラムがありません。\n必要: {required_columns}\n存在: {set(df.columns)}")
                
        except Exception as e:
            st.error(f"CSVファイルの読み込みに失敗しました: {e}")

# --- イベントフィルター ---
filtered_events = []
for e in st.session_state.events:
    if e["genre"] in genre_filter:
        event_copy = e.copy()
        event_copy["color"] = COLOR_MAP.get(e["genre"], "gray")
        filtered_events.append(event_copy)

# --- カレンダー表示 ---
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

# --- 編集・削除 ---
st.subheader("📝 イベント一覧・編集・削除")

if st.session_state.events:
    for idx, e in enumerate(st.session_state.events):
        with st.expander(f"{e['title']} ({e['start']})"):
            new_title = st.text_input(f"タイトル (index {idx})", e['title'], key=f"title_{idx}")
            new_date = st.date_input(f"日付 (index {idx})", datetime.date.fromisoformat(e['start']), key=f"date_{idx}")
            new_genre = st.selectbox(f"ジャンル (index {idx})", GENRES, index=GENRES.index(e['genre']), key=f"genre_{idx}")
            new_registration = st.selectbox(f"事前申し込み (index {idx})", ["必要", "不要"], index=["必要", "不要"].index(e['registration']), key=f"reg_{idx}")

            col1, col2 = st.columns(2)
            with col1:
                if st.button("更新", key=f"update_{idx}"):
                    st.session_state.events[idx] = {
                        "title": new_title,
                        "start": new_date.isoformat(),
                        "genre": new_genre,
                        "registration": new_registration
                    }
                    st.success(f"{new_title} を更新しました。")
                    st.rerun()

            with col2:
                if st.button("削除", key=f"delete_{idx}"):
                    deleted_title = st.session_state.events[idx]["title"]
                    st.session_state.events.pop(idx)
                    st.success(f"{deleted_title} を削除しました。")
                    st.rerun()
else:
    st.info("イベントがありません。サイドバーから新しいイベントを追加してください。")