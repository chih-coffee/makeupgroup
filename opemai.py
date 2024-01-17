import pandas as pd
import openai
import re
import time

openai.api_key = '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'

def remove_image_links(text):
    return re.sub(r'https?://\S+', '', text)

def fetch_analysis_from_openai(content):
    try:
        content_without_images = remove_image_links(content)

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            max_tokens=512,
            temperature=0,
            messages=[
                {"role": "user", "content": "分析文章，回傳抓取到的資料，只需回傳品牌、名稱、種類(眼影、唇彩、底妝、眉筆、眼線、睫毛膏、其他)，例如:ETUDE&膜幻濾鏡透感唇霧&唇彩"},
                {"role": "assistant", "content": "品牌&名稱&種類&,品牌&名稱&種類"},
                {"role": "user", "content": "各產品用逗號開"},
                {"role": "user", "content": content_without_images[:500]}
            ]
        )
        assistant_reply = response['choices'][0]['message']['content']

       
        return assistant_reply

    except Exception as e:
        print(f"處理內容時發生錯誤: {content}")
        print(f"錯誤: {e}")
        return "分析: 不明"

def read_local_data_and_analyze():
    articles_data = []
    df = pd.read_excel('demo.xlsx')

    for index, row in df.iterrows():
        content = row.get('內容', '')
        if content:
            analysis = fetch_analysis_from_openai(content)
            articles_data.append({
                '標題': row.get('標題', ''),
                '內容': content,
                '年份': row.get('年份', ''),
                '分析': analysis, 
                '類別': row.get('類別', ''),
                '人氣': row.get('人氣', ''),
                '日期': row.get('日期', ''),
                '網址': row.get('網址', '')
            })
            time.sleep(1)  # 增加请求之间的延迟

    return articles_data

def write_to_excel(articles_data):
    df = pd.DataFrame(articles_data)
    df.to_excel("demo.xlsx", index=False, engine='openpyxl')

def main():
    articles_data = read_local_data_and_analyze()
    write_to_excel(articles_data)

if __name__ == "__main__":
    main()
