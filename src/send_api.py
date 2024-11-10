# APIによるデータ取得

# インポート
import streamlit as st
import requests
import pandas as pd
from src.pref_data import pref_id, change_index

# apiキーの取得
api_key = st.secrets["api_key"]
my_url = st.secrets["my_url"]


# API接続関数
def connect_api(api_key: str | int, prefecture: str, city: str | None, year: int):
    api_key = api_key
    url = "https://www.reinfolib.mlit.go.jp/ex-api/external/XIT002"
    headers = {"Ocp-Apim-Subscription-Key": f"{api_key}"}
    params = {"year": year, "area": pref_id[prefecture]}
    response = requests.get(url, headers=headers, params=params)
    json_data = response.json()

    #  市町村コードの取得
    def send_city_id(json_data, city: str | None):
        try:
            for item in json_data["data"]:
                if city == "":
                    return None
                if city in item["name"]:
                    return item["id"]
                if city == "":
                    return None
            else:
                return "該当する市町村が存在しません"
        except KeyError:
            return "該当する市町村が存在しません"

    #  入力された市町村が存在しない場合
    city_id = send_city_id(json_data, city)
    url = "https://www.reinfolib.mlit.go.jp/ex-api/external/XIT001"
    params["city"] = city_id
    response = requests.get(url, headers=headers, params=params)
    json_data = response.json()

    #  検索結果に応じた内容を画面描画
    try:
        df = pd.DataFrame(json_data["data"])
        df["TradePrice"] = df["TradePrice"].apply(lambda x: f"¥{int(x):,}")
        df = df.drop(
            columns=[
                "PriceCategory",
                "Prefecture",
                "MunicipalityCode",
                "UnitPrice",
                "Frontage",
                "PricePerUnit",
            ]
        )
        df = df.rename(columns=change_index)
        df.rename(
            columns={"用途地区": "取引価格", "取引価格": "用途地区"}, inplace=True
        )
        df["取引価格"], df["用途地区"] = df["用途地区"], df["取引価格"]
        st.link_button("空き家を登録してみる（外部サイト）", url=my_url)
        st.write(f"{year}年の{prefecture}{city}の取引情報")
        st.write(f"取引件数{str(len(df))}件")
        st.dataframe(df)

    except KeyError:
        st.write("該当する市町村が存在しません")
