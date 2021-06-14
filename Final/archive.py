#!/usr/bin/env python
'''
@file:archive.py
@author: Honour-Van: fhn037@126.com
@description:将已有的几个有价值的数据导入的数据库中，包括微博语料、微博舆情、和热榜舆情
@version:1.0
'''


import sqlite3
import json
import pandas as pd
from sqlalchemy import create_engine

# 存入微博语料：武汉，从2019年12月初到2020年12月底
try:
    conn = sqlite3.connect('weibo_wuhan.db')
    print("Opened database successfully")
    curs = conn.cursor()
except:
    raise Exception("db init wrong")
# 创建语料表格
try:
    curs.execute(
        "CREATE TABLE if not exists wuhan2019(content TEXT, timestamp TEXT)")
    curs.execute(
        "CREATE TABLE if not exists wuhan2020(content TEXT, timestamp TEXT)")
except:
    raise Exception("table create wrong")

# 导入语料
with open("./data/date.json", 'r', encoding='utf-8') as f:
    date_list = json.load(f)
for item in date_list:
    timestamp = f'{item["year"]}-{str(int(item["month"])+1)}-{str(item["day"]+1)}'
    with open("./out/wuhan_day/" + timestamp + ".txt", 'r', encoding='utf-8') as f:
        for line in f.readlines():
            curs.execute(f'INSERT INTO wuhan{item["year"]} VALUES(?,?)', [
                         line.strip('\n'), timestamp])
print('insert data sucessfully')
conn.commit()
curs.execute('SELECT *FROM wuhan2019')
print(curs.fetchall())
print("Operation done successfully")
conn.close()

# 热榜的微博舆情统计
df = pd.DataFrame(
    columns=['Timestamp', "Positive Count", "Neutral Count", "Negative Count"])

# 导入目标时间节点的舆情分布数据
with open('./out/hotrank_stat.json', 'r', encoding='utf-8') as f:
    sentidata = json.load(f)

# 将json文件转换为对应的pandas.dataframe
for item in sentidata:
    timestamp = list(item.keys())[0]
    df = df.append({'Timestamp': timestamp, "Positive Count": item[timestamp][0],
                   "Neutral Count": item[timestamp][1], "Negative Count": item[timestamp][2]}, ignore_index=True)
print(df)
engine = create_engine('sqlite:///weibo_wuhan.db')
df.to_sql("hotrank_senti", engine)

print(pd.read_sql("hotrank_senti",engine))

# 按日的微博舆情统计
df = pd.DataFrame(
    columns=['Timestamp', "Positive Count", "Neutral Count", "Negative Count"])

# 导入目标时间节点的舆情分布数据
with open('./data/hour.json', 'r', encoding='utf-8') as f:
    hour_list = json.load(f)

# 将json文件转换为对应的pandas.dataframe
for item in hour_list[:-1]:
    timestamp = f'{item["year"]}-{str(int(item["month"])+1)}-{str(item["day"]+1)}-{item["hour"]}'
    with open('./out/wuhan_stat_hour/' + timestamp + '.json') as f:
        data = json.load(f)
        df = df.append({'Timestamp': timestamp, "Positive Count": data["hour positive count"],
                "Neutral Count": data["hour neutral count"], "Negative Count": data["hour negative count"]}, ignore_index=True)
print(df)
df.to_sql("byday_senti", engine)
