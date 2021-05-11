from flask import Flask, jsonify  # 新增代码。装入Flask
import pandas as pd

app = Flask(__name__)  # 新增代码


@app.route("/")  # 新增代码，对应执行root()函数
def root():
    return app.send_static_file("visual.html")


@app.route("/getData1")
def getData1():
    df = pd.read_csv("./out/PeopleInSubwayTime.csv")
    data = [df.iloc[:, 0].tolist(), df.iloc[:, 1].tolist()]
    print(data)
    return  jsonify(data)


@app.route("/getData2")
def getData2():
    df = pd.read_csv("./out/PeopleInSubwayCount.csv")
    data = [df.iloc[:, 0].tolist(), df.iloc[:, 1].tolist()]
    print(data)
    return jsonify(data)



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80, debug=True)
# eof
