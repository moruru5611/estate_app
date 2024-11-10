import streamlit as st
from src.send_api import connect_api
from src.pref_data import pref_id, change_index

# secrets.tomlの取得
api_key = st.secrets["api_key"]

# フッターのHTMLとCSS
footer = """
    <style>
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: #f1f1f1;
        color: black;
        text-align: center;
        padding: 10px;
    }
    </style>
    <div class="footer">
        <p>不動産価格（取引価格・成約価格）情報取得API（国土交通省）を基に、作成しています。</p>
    </div>
    """

# フッターを挿入
st.markdown(footer, unsafe_allow_html=True)

st.title("不動産取引情報検索")

input_col1, input_col2, input_col3 = st.columns(3)
with input_col1:
    prefecture = st.selectbox(
        label="都道府県", options=[index for index, i in pref_id.items()]
    )
with input_col2:
    city = st.text_input(label="市町村（空白、部分一致可）", placeholder="大阪市")
with input_col3:
    year = st.number_input(label="取引時期（西暦）", value=2024, step=0)

search = connect_api(api_key, prefecture, city, year) if st.button("検索") else None
