import streamlit as st
from time import sleep
from bs4 import BeautifulSoup
import requests
import pandas as pd
import base64


st.title('電話帳ナビ　スクレイピング')
items = st.number_input('取得件数を入力してください。', 1, 100, 1)
button = st.button('Start')
latest_interation = st.empty()
bar = st.progress(0)
n = items // 20
if (items % 20) != 0: n += 1


def main():
  d_list = []
  count = 0
  for i in range(n):
    url = 'https://www.telnavi.jp/search?q=%E6%8A%95%E8%B3%87' + f'&p={i+1}'
    print(url)
   
    header = {
        'User-Agent': 'Mozilla/5.0',
        "referer":url
    }
    try:
      sleep(7)
      r = requests.get(url, headers=header, timeout=20)
      r.raise_for_status()
      soup = BeautifulSoup(r.content, 'lxml')
    except Exception as e:
      try:
        print('-----ERROR(リトライ中)-----')
        sleep(10)
        r = requests.get(url, headers=header, timeout=20)
        r.raise_for_status()
        soup = BeautifulSoup(r.content, 'lxml')
      except Exception as e:
        print('-----ERROR(リトライ中)-----')
        sleep(10)
        r = requests.get(url, headers=header, timeout=20)
        r.raise_for_status()
        soup = BeautifulSoup(r.content, 'lxml')
        pass
      pass

    jobs = soup.select('ul.entry_search_result > li') #td.entry_name
    print(len(jobs))

    for job in jobs:
      count += 1
      if count > items:
        break
      print('-'*30, count, '-'*30)
      company_name = job.select_one('td.entry_name').text
      company_name = ','.join(company_name.split()).replace(',', '')
      print(company_name)
      tel = job.select_one('td.entry_number a:nth-of-type(2)').text
      print(tel)
            
      d_list.append({
            '事業者名': company_name,
            '電話番号': tel,
        })
      bar.progress((count*100)//items)
      
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
