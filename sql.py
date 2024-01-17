import sqlite3
import pandas as pd

df = pd.read_excel('raw.xlsx')  # 讀取CSV檔

conn = sqlite3.connect('DATA.db')  # 連線至data base

cursor = conn.cursor()

cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='RAW'")
result_raw = cursor.fetchone()

if result_raw:
    cursor.execute('DELETE FROM RAW')  # 如果表格存在，刪除表格內的資料
else:
    cursor.execute('CREATE TABLE RAW(標題 TEXT, 人氣 INTEGER, 網址 TEXT)')  # 如果表格不存在，創建表格

df.to_sql('RAW', conn, if_exists='append', index=False)  # 將資料寫入表格

df = pd.read_excel('output_brand.xlsx') 
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='detail'")
result_detail = cursor.fetchone()

if result_detail:
    cursor.execute('DELETE FROM detail')  # 如果表格存在，刪除表格內的資料
else:
    cursor.execute('CREATE TABLE detail(標題 TEXT, 品牌 TEXT, 產品 TEXT, 種類 TEXT)')  # 如果表格不存在，創建表格

df.to_sql('detail', conn, if_exists='append', index=False)

cursor.execute("SELECT name, type FROM sqlite_master WHERE type = 'view' AND name LIKE 'step1';")
result_step1 = cursor.fetchone()
if result_step1:
    cursor.execute("DROP VIEW IF EXISTS step1;")
cursor.execute('''CREATE VIEW step1 as 
SELECT 
    標題,upper(品牌) as 品牌,
    CASE 
        WHEN substr(種類,1,1)='粉' or 種類='底妝' or 種類='腮紅'or substr(種類,1,2)='遮瑕'or substr(種類,1,2)='修容'or substr(種類,1,2)='定妝' or substr(種類,1,2)='打亮'THEN '底妝'
        WHEN substr(種類,1,2)='眼線' THEN '眼線'
        WHEN substr(種類,1,2)='眼影' THEN '眼影'
        WHEN substr(種類,1,1)='眉' THEN '眉筆'
        WHEN substr(種類,1,1)='唇' or substr(種類,1,1)='口' THEN '唇彩'
		WHEN substr(種類,1,2)='睫毛' THEN '睫毛膏'
        ELSE '其他'
    END AS 種類
FROM detail
where 品牌<>'不明'and 品牌<>'未提及'and 品牌<>'無'
''')
cursor.execute("SELECT name, type FROM sqlite_master WHERE type = 'view' AND name LIKE 'final';")
result_final = cursor.fetchone()

if result_final:
    cursor.execute("DROP VIEW IF EXISTS final")

cursor.execute ('''
CREATE VIEW final as 
select * from (select * from (
select *,row_number() over (order by 人氣 desc) as rank  from (
select 品牌,種類,group_concat(網址,'/n') as 網址,sum(人氣) as 人氣
from (
select a.*,b.品牌,b.種類
from raw  a 
left join step1 b
on a.標題 = b.標題)
where 品牌 is not null and 種類='底妝'
group by 品牌,種類
order by 人氣 desc)
order by 人氣 desc)
where rank <=5
UNION
select * from (
select *,row_number() over (order by 人氣 desc) as rank  from (
select 品牌,種類,group_concat(網址,'/n') as 網址,sum(人氣) as 人氣
from (
select a.*,b.品牌,b.種類
from raw  a 
left join step1 b
on a.標題 = b.標題)
where 品牌 is not null and 種類='眉筆'
group by 品牌,種類
order by 人氣 desc)
order by 人氣 desc)
where rank <=5
UNION
select * from (
select *,row_number() over (order by 人氣 desc) as rank  from (
select 品牌,種類,group_concat(網址,'/n') as 網址,sum(人氣) as 人氣
from (
select a.*,b.品牌,b.種類
from raw  a 
left join step1 b
on a.標題 = b.標題)
where 品牌 is not null and 種類='眼線'
group by 品牌,種類
order by 人氣 desc)
order by 人氣 desc)
where rank <=5
UNION
select * from (
select *,row_number() over (order by 人氣 desc) as rank  from (
select 品牌,種類,group_concat(網址,'/n') as 網址,sum(人氣) as 人氣
from (
select a.*,b.品牌,b.種類
from raw  a 
left join step1 b
on a.標題 = b.標題)
where 品牌 is not null and 種類='睫毛膏'
group by 品牌,種類
order by 人氣 desc)
order by 人氣 desc)
where rank <=5
UNION
select * from (
select *,row_number() over (order by 人氣 desc) as rank  from (
select 品牌,種類,group_concat(網址,'/n') as 網址,sum(人氣) as 人氣
from (
select a.*,b.品牌,b.種類
from raw  a 
left join step1 b
on a.標題 = b.標題)
where 品牌 is not null and 種類='眼影'
group by 品牌,種類
order by 人氣 desc)
order by 人氣 desc)
where rank <=5
UNION
select * from (
select *,row_number() over (order by 人氣 desc) as rank  from (
select 品牌,種類,group_concat(網址,'/n') as 網址,sum(人氣) as 人氣
from (
select a.*,b.品牌,b.種類
from raw  a 
left join step1 b
on a.標題 = b.標題)
where 品牌 is not null and 種類='唇彩'
group by 品牌,種類
order by 人氣 desc)
order by 人氣 desc)
where rank <=5
UNION
select * from (
select *,row_number() over (order by 人氣 desc) as rank  from (
select 品牌,種類,group_concat(網址,'/n') as 網址,sum(人氣) as 人氣
from (
select a.*,b.品牌,b.種類
from raw  a 
left join step1 b
on a.標題 = b.標題)
where 品牌 is not null and 種類='其他'
group by 品牌,種類
order by 人氣 desc)
order by 人氣 desc)
where rank <=5)
order by 種類,rank

''')

cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='final_table'")
result_raw = cursor.fetchone()

if result_raw:
    cursor.execute('drop table final_table')  # 如果表格存在，刪除表格內的資料

cursor.execute('CREATE TABLE final_table AS SELECT * FROM final;') 

conn.commit()  # 儲存至DATA BASE

cursor.close()
conn.close()  # 關閉連線
