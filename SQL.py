import sqlite3
import pandas as pd

df = pd.read_csv('demo.csv') #讀取CSV檔

conn = sqlite3.connect('DATA.db') #連線至data base

cursor = conn.cursor() #
cursor.execute('CREATE TABLE DEMO(年份,日期,類別,標題,人氣,網址,情感分析,關鍵句子,內容)') #新建Table

df.to_sql('DEMO',conn, if_exists='append',index=False) #如果資料表存在，就寫入資料，否則建立資料

cursor.execute('''CREATE VIEW FINAL_BASE AS 
SELECT 類別, SUBSTR(日期, 1, 2) AS 月份, COUNT(標題) AS 數量,GROUP_CONCAT(標題,' / ') AS 標題
FROM DEMO
GROUP BY 類別, SUBSTR(日期, 1, 2)
ORDER BY 月份''') #建立view表

conn.commit() #儲存至DATA BASE
us_df = pd.read_sql("SELECT * FROM FINAL_BASE ", conn) #SHOW VIEW
print(us_df) #在終端機顯示該VIEW
conn.close() #關閉連線

##只要執行一次就好，不然會重複寫入


