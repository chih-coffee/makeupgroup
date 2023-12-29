
import requests
from bs4 import BeautifulSoup
from snownlp import SnowNLP
import csv
from time import sleep
from random import uniform
import re

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'}

def fetch_url(url):
    return requests.get(url, headers=headers)

def parse_article_details(soup):  # 內文
    try:
        header = soup.find_all('span', 'article-meta-value')
        title = header[2].text.split("]")[1].strip()
        main_container = soup.find(id='main-container')
        raw_content = main_container.text
        re_date = re.search(r'時間(.+?)\n', raw_content)
        date = re_date.group(1)[-4:]
        all_text = main_container.text.split('--')[0]
        # 去頭
        contents = all_text.split('\n')[2:]
        content = '\n'.join(contents)
        s = SnowNLP(content)
        summary = s.summary(3)  # 提取三個關鍵句子
        sentiment = s.sentiments  # 情感分析
        return {'標題': title, '內容': content, '關鍵句子': summary, '情感分析': sentiment,'年份':date}
    except Exception as e:
        return {'錯誤': str(e)}

def get_articles_from_page(page_number):
    articles_data = []
    base_url = "https://www.ptt.cc"
    url = f"{base_url}/bbs/MakeUp/index{page_number}.html"
    response = fetch_url(url)
    soup = BeautifulSoup(response.text, "html.parser")

    sections = soup.select('div.r-ent')
    keys = ["[選擇]", "[心得]", "[妝容]"]
    for section in sections:
        num = section.find('div', class_="nrec").text
        if num == '爆' or (num.isdigit() and int(num) >= 10):
            title = section.select('div.title')[0].text.strip()
            for key in keys:
                if key in title:
                    link = section.find('a')['href']
                    article_soup = fetch_url(base_url + link).text
                    article_details = parse_article_details(BeautifulSoup(article_soup, "html.parser"))
                    article_details['類別'] = key.strip('[]')
                    article_details['人氣'] = num
                    article_details['日期'] = section.find("div", class_="date").text
                    articles_data.append(article_details)
    return articles_data

start_page = 3850
end_page = 3851

all_articles = []
for page in range(start_page, end_page + 1):
    all_articles.extend(get_articles_from_page(page))
    sleep(uniform(0.4, 1))

filenames = ["標題", "類別", "內容", "人氣", "日期", "關鍵句子", "情感分析","年份"]

# 開啟 CSV 檔案，將 'a+' 改為 'w'，以確保每次都是重新寫入
with open("demo.csv", "w", newline="", encoding='UTF-8') as file:
    # 使用 DictWriter 寫入 CSV
    writor = csv.DictWriter(file, fieldnames=filenames)

    # 寫入 CSV 標題
    writor.writeheader()

    # 在寫入 CSV 之前將數據轉換為 'cp950' 編碼
    all_articles_cp950 = []
    for article in all_articles:
        article_cp950 = {key: value.encode('cp950', errors='replace').decode('cp950') if isinstance(value, str) else value for key, value in article.items()}
        all_articles_cp950.append(article_cp950)

    # 寫入數據
    writor.writerows(all_articles_cp950)
