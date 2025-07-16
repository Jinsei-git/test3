import streamlit as st
from streamlit.components.v1 import html
import json
import pandas as pd
from datetime import datetime, timedelta
import uuid


# ページ設定
st.set_page_config(
    page_title="スマートカレンダー",
    page_icon="📅",
    layout="wide"
)

 
st.title("📅 スマートカレンダー - クリックで予定追加")


# セッション状態の初期化
if "events" not in st.session_state:
    st.session_state.events = []
 

# サイドバー - コントロールパネル
st.sidebar.header("🎛️ コントロールパネル")


# CSVファイルアップロード
uploaded_file = st.sidebar.file_uploader(
    "📂 CSVファイルアップロード",
    type=['csv'],
    help="予定CSVファイルをアップロードしてカレンダーに追加してください"
)

 
def create_sample_csv():
    """サンプルCSV生成"""
    sample_data = {
        'title': ['チームミーティング', 'プロジェクト発表', '昼食約束'],
        'start_date': ['2024-07-20', '2024-07-22', '2024-07-25'],
        'start_time': ['14:00', '10:00', '12:30'],
        'end_date': ['2024-07-20', '2024-07-22', '2024-07-25'],
        'end_time': ['15:00', '11:30', '13:30'],
        'description': ['週次チームミーティング', 'プロジェクト発表', '同僚との昼食'],
        'color': ['#FF6B6B', '#4ECDC4', '#45B7D1'],
        'category': ['会議', '業務', '個人']
    }
    return pd.DataFrame(sample_data)