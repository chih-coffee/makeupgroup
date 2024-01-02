# save this as app.py
from flask import Flask,render_template,request,json,jsonify
import sqlite3
app = Flask(__name__)
# app.config['JSON_AS_ASCII']=False
@app.route("/")
def hello():
    return render_template("home.html")

@app.route("/result",methods=['GET'])
def Result():
    if request.method=="GET":
        connection=sqlite3.connect("DATA.db")
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM `DEMO`;')
        results=cursor.fetchall()
        lstdata=[]
        d=dict()
        for row in results:
            year,date,tp,title,famous,url,emo,keyword,content=row
            d["年份"]=year
            d["日期"]=date
            d["類別"]=tp
            d["標題"]=title
            d["人氣"]=famous
            d["網址"]=url
            d["情感分析"]=emo
            d["關鍵句子"]=keyword
            # d["內容"]=content
            lstdata.append(d)
            print(d)
        # data=jsonify(lstdata)
        jsondata=json.dumps(lstdata,ensure_ascii=False)
        # data=jsonify(jsondata,ensure_ascii=False)
        cursor.close()  
        connection.close()
    return jsondata
@app.route("/<name>")#名字回傳
def getname(name):
    return f"UserName is : {name}"

@app.route("/<int:num>")#數字回傳
def getnum(num):
    return f"Number is : {num}"

if __name__=='__main__':#主程式
    app.run()