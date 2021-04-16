from flask import Flask, request, render_template
import pandas as pd


def read_data() -> pd.DataFrame:
    with open('poetScore.txt', 'r', encoding='utf-8') as f:
        df = pd.DataFrame(pd.read_csv('poetScore.txt'))
    df.insert(4, '总成绩', [round(int(row['平时成绩'])*0.3+int(row['期中成绩'])*0.3+int(row['期末成绩'])*0.4)
                         for _, row in df.iterrows()])
    return df


def choose_color(grade):
    if grade >= 85:
        return 'Green'
    elif grade >= 60:
        return 'Yellow'
    else:
        return 'Red'


def draw_table(df: pd.DataFrame, sortby:str) -> str:
    rowdata = ''
    for _, row in df.iterrows():
        rowunit = f"<tr id='rd'><td>{row['姓名']}</td><td>{row['平时成绩']}</td><td>{row['期中成绩']}</td><td>{row['期末成绩']}</td><td>{row['总成绩']}</td>"
        if sortby == "姓名":
            rowdata += rowunit
            rowdata += '</tr>'
        else:
            vis = row[sortby]
            color = choose_color(vis)
            rowunit += f"<td><div class='stateDiv' style='background:{color}; width:{vis}px;'></div></td></tr>"
            rowdata += rowunit
    return rowdata


app = Flask(__name__)


@app.route("/")
def root():
    df1 = read_data().sort_values(by="总成绩", ascending=False)
    rowdata = draw_table(df1,"总成绩")
    return render_template('render.html', row=rowdata)


@app.route("/sortby", methods=("post",))
def sortBy():
    sb = request.form["Basis"]
    asd = int(request.form["Ascending"])
    df2 = read_data().sort_values(by=sb, ascending=asd)
    rowdata = draw_table(df2,sb)
    return rowdata


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80, debug=True)
