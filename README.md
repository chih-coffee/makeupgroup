# MakeupGroup

歡迎來到MakeupGroup，美妝產品推陳出新，市面上產品百百種，如何快速知道目前市面上最受歡迎的產品？
本專案爬蟲了 2023年整年度 PTT 美妝版網友討論的文章， 利用Python將PTT美妝版所提及的商品做分數評價，並根據品牌做排行榜分享給使用者
將產品分門別類，並依照「人氣」、「被提及的次數」，去做排名，為聚焦在產品聲量，僅討論「心得」、「選擇」、「妝容」的類別。 

由chih-coffee/ emmchou/ yiiiiii06/ d8a2v8i1d4共同開發，包括多種工具和分析，旨在探索化妝行業的趨勢、偏好和見解。

## 特色

- **數據分析**：通過我們詳細的Jupyter Notebook和Python腳本深入了解美妝趨勢。
- **網頁應用**：通過用戶友好的網頁界面像是Flask與HTML 顯示成果。
- **全面數據**：探索2023年的美妝數據，包括詳細分析和視覺化。

## 安裝

具體安裝步驟取決於您感興趣的組件，因此請參閱存儲庫中的個別文件說明以獲取更多詳細訊息。

1.執行 爬取2023 美妝資料.ipynb，命名為FINAL.xlsx

2.執行pivot.py，將FINAL.xlsx資料做切割，解決一篇文章有多個產品的問題，產生output_brand.xlsx

3.執行sql.py，將整理好的資料放進DB裡面，並做整理和分析

4.將網頁的html架好，update_web.html

5.執行update_app.py


bash
git clone https://github.com/chih-coffee/makeupgroup.git
cd makeupgroup

## 使用

要開始探索化妝數據和分析，請按照存儲庫文檔中的說明打開Jupyter Notebook或運行網頁應用。

## 貢獻

歡迎貢獻！如果您對新功能、改進或錯誤修復有任何想法，請隨時分叉存儲庫並提交拉取請求。

## 許可

此項目根據MIT許可證的條款授權。

## 聯繫

如有任何問題或建議，請在GitHub上開一個問題進行進一步討論。
訪問我們的[GitHub存儲庫](https://github.com/chih-coffee/makeupgroup)以獲取更多信息並開始使用！
