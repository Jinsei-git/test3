import streamlit as st

st.title("Streamlit Selectbox Showcase")

st.header("1️. Selectbox（単一選択）")
option = st.selectbox(
    '好きなフルーツを選んでください:',
    ['りんご', 'バナナ', 'オレンジ', 'メロン']
)
st.write('選択されたのは:', option)

st.header("2️. Radio（単一選択）")
radio_option = st.radio(
    "好きな色は？",
    ['赤', '青', '緑']
)
st.write("選んだ色:", radio_option)

st.header("3️. Multiselect（複数選択）")
multi_options = st.multiselect(
    '好きなスポーツを選択:',
    ['サッカー', '野球', 'バスケ', 'テニス', '水泳']
)
st.write("選んだスポーツ:", multi_options)

st.header("4️. スライダー（数値選択）")
number = st.slider(
    '数を選んでください',
    min_value=0, max_value=100, value=50
)
st.write("選んだ数:", number)

st.header("5️. スライダー（範囲選択）")
range_values = st.slider(
    '範囲を選んでください',
    min_value=0, max_value=100, value=(20, 80)
)
st.write("選んだ範囲:", range_values)

st.header("6️. Select_slider（順序付き選択）")
level = st.select_slider(
    '難易度を選んでください',
    options=['簡単', '普通', '難しい', '超難しい'],
    value='普通'
)
st.write('選んだ難易度:', level)

st.header("7️. チェックボックスで選択肢を制御")
if st.checkbox("詳細オプションを表示"):
    detail_option = st.radio("追加オプション:", ['Option A', 'Option B', 'Option C'])
    st.write("詳細オプション:", detail_option)

st.header("8️. Cascading（依存型選択）")
country = st.selectbox("国を選んでください", ['日本', 'アメリカ'])
if country == '日本':
    city = st.selectbox("日本の都市:", ['東京', '大阪', '京都'])
else:
    city = st.selectbox("アメリカの都市:", ['ニューヨーク', 'ロサンゼルス', 'シカゴ'])

st.write(f"選んだ国: {country}, 都市: {city}")
