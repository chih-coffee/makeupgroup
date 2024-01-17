import pandas as pd

# 讀取 Excel 文件
df = pd.read_excel('FINAL.xlsx')

# 重新組織資料
new_rows = []

for index, row in df.iterrows():
    title = row['標題']
    ana_values = row['分析'].split('\n\n')
    
    for value in ana_values:
        new_rows.append({'標題': title, '分析': value})

# 創建新的 DataFrame
new_df = pd.DataFrame(new_rows)

# 將結果寫入新的 Excel 文件
new_df.to_excel('output_file.xlsx', index=False)
# 讀取 Excel 文件
df = pd.read_excel('output_file.xlsx')

# 重新組織資料
new_rows = []

for index, row in df.iterrows():
    title = row['標題']
    ana_values = row['分析']
    brand_match = match = re.search(r'品牌:\s*([^名稱]+)名稱:', ana_values)
    product_match = match = re.search(r'名稱:\s*([^種類]+)', ana_values)
    item_match = match = re.search(r'種類:\s*(.+)', ana_values)

    if brand_match:
        brand = brand_match.group(1).strip()
    else:
        brand ='Na'
    if product_match:
        product = product_match.group(1).strip()
    else:
        product ='Na'
    if item_match:
        item = item_match.group(1).strip()
    else:
        item ='Na'

    new_rows.append({'標題': title, '品牌': brand,'產品':product,'種類':item,'分析':ana_values})
    


# 創建新的 DataFrame
new_df = pd.DataFrame(new_rows)

# 將結果寫入新的 Excel 文件
new_df.to_excel('output_brand.xlsx', index=False)
