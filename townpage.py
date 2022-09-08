import streamlit as st
from inspect import isframe
from time import sleep, time
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from lib2to3.pgen2 import driver
import pandas as pd
import base64

st.title('iタウンページ　スクレイピング')
items = st.number_input('取得件数を入力してください。', 1, 100000, 1)
button = st.button('Start')
latest_interation = st.empty()
bar = st.progress(0)
n = items // 20
if (items % 20) != 0: n += 1

def main():
  # Firefox のオプションを設定する
  # (現在Windows(WSL2)のdockerだとchromeが使えないです)
  options = webdriver.FirefoxOptions()

  # Selenium Server に接続する
  driver = webdriver.Remote(
      command_executor='http://localhost:4444/wd/hub',
      options=options,
  )

  # Selenium 経由でブラウザを操作する
  # options = Options()
  # options.add_argument('--headless')
  # options.add_argument('--incognito')
  # options.add_argument('--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.128 Safari/537.36')

  # driver = webdriver.Chrome(
  #   executable_path = ChromeDriverManager().install(),
  #   options = options)
  # driver.implicitly_wait(10)
  url = 'https://itp.ne.jp/keyword/?keyword=%E7%BE%8E%E5%AE%B9%E9%99%A2&areaword=%E6%9D%B1%E4%BA%AC%E9%83%BD&sort=01&sbmap=false%EF%BC%88%E7%BE%8E%E5%AE%B9%E9%99%A2'

  driver.get(url)
  sleep(3)

  page_count = 0
  for i in range(1, n, 1):
    btn_box = driver.find_element(By.CSS_SELECTOR, 'button.m-read-more')
    btn_box.click()
    sleep(5)
    page_count += 1
    v = (i / (n-1)) * 100
    bar.progress(int(v))

  d_list = []
  count = 0
  r = driver.page_source
  soup = BeautifulSoup(r, 'lxml')
  jobs = soup.select('li.o-result-article-list__item')
  # print(len(jobs))

  for job in jobs:
    count += 1
    if count > items:
      break
    
    print('-'*30, count, '-'*30)
    company_name = job.select_one('h2.m-article-card__header__title').text
    company_name = ','.join(company_name.split()).replace(',', '')
    print(company_name)

    tel_elem = job.select_one('p.m-article-card__lead__caption:-soup-contains(電話番号)')
    if tel_elem:
      tel = tel_elem.text.split()[1]
      print(tel)
    address = job.select_one('p.m-article-card__lead__caption:-soup-contains(住所)')
    if address:
      address = address.text
      address = ','.join(address.split()).replace(',', '').replace('【住所】', '')
      print(address)
    
    d_list.append({
          '店舗名': company_name,
          '電話番号': tel,
          '住所': address
      })
    
    df = pd.DataFrame(d_list)
  return df
#       # df.to_csv(csv_name, index=False, encoding='utf-8-sig')

if button:
  df = main()
  st.write('## スクレイピング結果', df)
  '完了'
  csv = df.to_csv(index=False, encoding='utf-8-sig')  
  b64 = base64.b64encode(csv.encode('utf-8-sig')).decode()
  href = f'<a href="data:application/octet-stream;base64,{b64}" download="result.csv">download</a>'
  st.markdown(f"ダウンロードする {href}", unsafe_allow_html=True)
