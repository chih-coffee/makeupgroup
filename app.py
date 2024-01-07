# save this as app.py
from flask import Flask,render_template,request,json,jsonify
import sqlite3
app = Flask(__name__)
# app.config['JSON_AS_ASCII']=False
@app.route("/")
def hello():
    return render_template("home.html")

@app.route("/result",methods=['GET','POST'])
def Result():
    if request.method=="GET":
        return render_template("web.html",start="起動成功")

    elif request.method=="POST":
        connection=sqlite3.connect("DATA.db")
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM `DEMO`;')
        results=cursor.fetchall()
        button1=request.values.get("口紅")
        button2=request.values.get("底妝")
        button3=request.values.get("彩妝")
        alldata=[]
        for row in results:
            year,date,tp,title,famous,url,emo,keyword,content=row
            d=dict()
            # year,date,num,title=row
            d["年份"]=year
            d["日期"]=date
            d["類別"]=tp
            d["標題"]=title
            d["人氣"]=famous
            d["網址"]=url
            d["情感分析"]=emo
            d["關鍵句子"]=keyword
            d["內容"]=content
            alldata.append(d)
        if button1=="口紅":
            data=[i for i in alldata if i["類別"]=="口紅"]
            return render_template("web.html",data=data)
        elif button2=="底妝":
            data=[i for i in alldata if i["類別"]=="底妝"]
            return render_template("web.html",data=data)
        elif button3=="彩妝":
            data=[i for i in alldata if i["類別"]=="彩妝"]
            return render_template("web.html",data=data)
        cursor.close()  
        connection.close()

@app.route("/<name>")#名字回傳
def getname(name):
    return f"UserName is : {name}"

@app.route("/<int:num>")#數字回傳
def getnum(num):
    return f"Number is : {num}"

if __name__=='__main__':#主程式
    app.run()

#執行完後去網頁127.0.0.1/5000/result