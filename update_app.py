from flask import Flask, render_template, request, jsonify
import sqlite3

app = Flask(__name__)

@app.route("/")
def hello():
    return render_template("home.html")

@app.route("/result", methods=['GET', 'POST'])
def Result():
    if request.method == "GET":
        return render_template("home.html", start="起動成功")

    elif request.method == "POST":
        connection = sqlite3.connect("DATA.db")
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM `new_final`;')
        results = cursor.fetchall()
        alldata = []

        for row in results:
            tp, famous, rank, keyword, url = row
            d = {
                "品牌": tp,
                "種類": famous,
                "排名": url,
                "網址": rank,
                "人氣": keyword
            }
            alldata.append(d)

        button_values = {
            "底妝": "底妝",
            "眉筆": "眉筆",
            "眼影": "眼影",
            "眼線": "眼線",
            "唇彩": "唇彩",
            "睫毛膏": "睫毛膏",
            "其他": "其他"
        }

        selected_button = None
        for button, value in button_values.items():
            if request.values.get(button) == value:
                selected_button = value
                break

        if selected_button:
            data = [i for i in alldata if i["種類"] == selected_button]
            return render_template("home.html", data=data)

        cursor.close()
        connection.close()

        return jsonify([])  # 添加这行返回语句

if __name__ == '__main__':
    app.run()
