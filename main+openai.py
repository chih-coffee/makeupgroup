import requests
from bs4 import BeautifulSoup
import csv
from time import sleep
import re
import openai
openai.api_key = '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'

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
        
        # openai回傳產品名稱、種類、評分
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            max_tokens=512,
            temperature=0,
            messages=[
                {"role": "user", "content": "分析文章，回傳抓取到的資料，只需回傳品牌、名稱、種類(眼影、唇彩、底妝、眉筆、眼線、睫毛膏)及判斷文章語句對產品的評分(1-5分)，若未知請填'未知"},
                {"role": "assistant", "content": "品牌:\n名稱:\n種類:\n評分:"},
                {"role": "user", "content": content}
            ]
        )
        assistant_reply = response['choices'][0]['message']['content']
        assistant_reply = assistant_reply.split('\n')
        #將openai回覆的文字分門別類
        brand_name = assistant_reply[0][4:]
        product_name = assistant_reply[1][4:]
        product_category = assistant_reply[2][4:]
        product_score = assistant_reply[3][4:]
        sleep(20)
        
        return {'標題': title, '內容': content, '年份':date, '品牌':brand_name, '產品名稱':product_name, '產品種類':product_category,'評分':product_score}
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
                    article_details['網址'] ="https://www.ptt.cc" + link
                    articles_data.append(article_details)
    return articles_data

#前一頁頁數
url = 'https://www.ptt.cc/bbs/MakeUp/index.html'
soup = BeautifulSoup(fetch_url(url).text, "html.parser")
previous_page = soup.select('div#action-bar-container div.btn-group-paging a')[1]['href']
previous_page_num = int(previous_page.replace('/bbs/MakeUp/index','').replace('.html',''))
#最新頁數
page = previous_page_num + 1 

all_articles = []
for i in range(2): #抓2頁
    page -= i
    all_articles.extend(get_articles_from_page(page))
    

filenames = ["標題", "類別", "產品種類", "品牌", "產品名稱", "內容", "人氣", "日期", "評分", "年份", "網址"]

# 開啟 CSV 檔案，將 'a+' 改為 'w'，以確保每次都是重新寫入
with open("Demo.csv", "w", newline="", encoding='UTF-8') as file:
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
