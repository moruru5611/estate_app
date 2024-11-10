from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep

url="https://estateapp.streamlit.app/" 
options = Options()

# ヘッドレスモード（Linux上で動かすとき必ずこのモードにしておく）
options.add_argument('--headless')

# URLへアクセス
driver = webdriver.Chrome(options=options)

# 暗黙的な待機時間を設定
driver.implicitly_wait(120)
driver.get(url)
print(driver.current_url)

# 30秒待機した後に、ブラウザを閉じる
sleep(30)
driver.quit()