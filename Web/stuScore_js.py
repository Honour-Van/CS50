from flask import Flask, jsonify, render_template
import studScore as sc
import pandas as pd
from xpinyin import Pinyin


def read_data() -> pd.DataFrame:
    with open('poetScore.txt', 'r', encoding='utf-8') as f:
        df = pd.DataFrame(pd.read_csv('poetScore.txt'))
    df.insert(4, '总成绩', [round(int(row['平时成绩'])*0.3+int(row['期中成绩'])*0.3+int(row['期末成绩'])*0.4)
                         for _, row in df.iterrows()])
    df.rename(columns={'姓名': 'name'}, inplace=True)
    p = Pinyin()
    df.insert(5, '姓名', [p.get_pinyin(row['name'], tone_marks='numbers')
                        for _, row in df.iterrows()])
    return df


app = Flask(__name__)


@app.route('/')
def root():
    return render_template('render2.html', data=read_data().to_json(orient='records', force_ascii=False))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80, debug=True)
