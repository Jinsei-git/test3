import streamlit as st
from streamlit_gsheets_connection import GSheetsConnection
import pandas as pd

# デバッグ情報を表示
st.title("Google Sheets連携テスト")

try:
    # 接続を作成
    st.write("🔄 Google Sheetsに接続中...")
    conn = st.connection("gsheets", type=GSheetsConnection)
    
    # データを読み込み
    st.write("📊 データを読み込み中...")
    df = conn.read()
    
    # 成功メッセージ
    st.success("✅ 接続成功！")
    
    # データの表示
    st.write("📋 読み込まれたデータ:")
    if df is not None and not df.empty:
        st.dataframe(df)
        
        # データの詳細情報
        st.write(f"**行数:** {len(df)}")
        st.write(f"**列数:** {len(df.columns)}")
        st.write(f"**列名:** {list(df.columns)}")
    else:
        st.warning("⚠️ データが空です")
        
except Exception as e:
    st.error(f"❌ エラーが発生しました:")
    st.code(str(e))
    
    # トラブルシューティング情報
    st.write("### 🔧 トラブルシューティング")
    
    # secrets.tomlの確認
    if hasattr(st, 'secrets') and 'connections' in st.secrets:
        if 'gsheets' in st.secrets['connections']:
            st.write("✅ secrets.tomlの設定が見つかりました")
            
            # 設定内容の確認（機密情報は隠す）
            gsheet_config = st.secrets['connections']['gsheets']
            st.write("📋 現在の設定:")
            for key in gsheet_config.keys():
                if key in ['private_key', 'client_email']:
                    st.write(f"- {key}: {'*' * 20}")
                else:
                    st.write(f"- {key}: {gsheet_config[key]}")
        else:
            st.write("❌ secrets.tomlに'gsheets'設定が見つかりません")
    else:
        st.write("❌ secrets.tomlファイルが見つかりません")
    
    # 設定例を表示
    with st.expander("📝 設定例"):
        st.markdown("""
        ### `.streamlit/secrets.toml` の設定例:
        
        **方法1: 公開されたスプレッドシートの場合**
        ```toml
        [connections.gsheets]
        spreadsheet = "あなたのスプレッドシートのURL"
        worksheet = "シート1"
        ```
        
        **方法2: サービスアカウントを使用する場合**
        ```toml
        [connections.gsheets]
        spreadsheet = "スプレッドシートID"
        worksheet = "シート1"
        type = "service_account"
        project_id = "your-project-id"
        private_key_id = "key-id"
        private_key = "-----BEGIN PRIVATE KEY-----\nYOUR_PRIVATE_KEY\n-----END PRIVATE KEY-----\n"
        client_email = "your-service-account@your-project.iam.gserviceaccount.com"
        client_id = "123456789"
        auth_uri = "https://accounts.google.com/o/oauth2/auth"
        token_uri = "https://oauth2.googleapis.com/token"
        auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
        ```
        """)
    
    with st.expander("📋 必要な手順"):
        st.markdown("""
        ### 設定手順:
        
        1. **Google Sheetsの準備:**
           - スプレッドシートを作成
           - データを入力（写真のような形式）
           - 「共有」→「リンクを知っている全員」に設定
        
        2. **フォルダ構造:**
           ```
           your_project/
           ├── gsheets_calendar1.py
           ├── requirements.txt
           └── .streamlit/
               └── secrets.toml
           ```
        
        3. **パッケージのインストール:**
           ```bash
           pip install streamlit st-gsheets-connection pandas
           ```
        
        4. **実行:**
           ```bash
           streamlit run gsheets_calendar1.py
           ```
        """)

# 更新ボタン   
if st.button("🔄 再試行"):
    st.rerun()
