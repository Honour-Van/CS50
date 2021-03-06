#!/usr/bin/env python
'''
@file:sentiment.py
@author: Honour-Van: fhn037@126.com
@description:进行语言情感识别
@version:1.0
'''


from senta import Senta
import json
from mytool import progress_bar

def preprocess(keyword):
    date_list = []
    with open('./data/date.json', 'r', encoding='utf-8') as f:
        date_list = json.load(f)
    l = len(date_list)

    pb = progress_bar(l)
    for i in range(l-1):
        y = date_list[i]['year']
        m = str(int(date_list[i]['month'])+1)
        d = str(date_list[i]['day']+1)
        day_sentences = []
        for h in range(24):
            hour_sentences = []
            try:
                with open(f'./out/{keyword}_raw/{y}-{m}-{d}-{h}.txt', 'r', encoding='utf-8') as f:
                    while True:
                        line = f.readline()
                        if line == '':
                            break
                        line = line.strip()
                        if line == '':
                            continue
                        elif "展开全文" in line:
                            continue
                        else:
                            if line not in hour_sentences:
                                hour_sentences.append(line)
                            if line not in day_sentences:
                                day_sentences.append(line)
            finally:
                with open(f'./out/{keyword}_hour/{y}-{m}-{d}-{h}.txt', 'w', encoding='utf-8') as fh:
                    for line in hour_sentences:
                        print(line, file=fh)
        pb.progress(i)

        with open(f'./out/{keyword}_day/{y}-{m}-{d}.txt', 'w', encoding='utf-8') as f:
            for line in day_sentences:
                print(line, file=f)


def senti_analysis(keyword):
    date_list = []
    with open('./data/date.json', 'r', encoding='utf-8') as f:
        date_list = json.load(f)
    l = len(date_list)

    senta = Senta()
    pb = progress_bar(l)

    mon_stat = {}
    for i in range(l-1):
        y = date_list[i]['year']
        m = str(int(date_list[i]['month'])+1)
        d = str(date_list[i]['day']+1)
        pb.progress(i)

        with open(f'./out/{keyword}_day/{y}-{m}-{d}.txt', 'r', encoding='utf-8') as f:
            senta.add(f.readlines())
        senta.predict()
        day_neg = 0
        day_pos = 0
        day_neu = 0
        pos_dis = {}
        for item in senta.results:
            positive_prob = round(item['positive_probs'], 2)
            negative_prob = round(item['negative_probs'], 2)
            pos_dis[positive_prob] = pos_dis.get(positive_prob, 0) + 1
            if positive_prob >= 0.85:
                day_pos += 1
            elif negative_prob >= 0.6:
                day_neg += 1
            else:
                day_neu += 1
        mon_id = f"{y}-{m}"
        if mon_id in mon_stat:
            mon_stat[mon_id]["positive cnt"] = mon_stat[mon_id]["positive cnt"] + day_pos
            mon_stat[mon_id]["neutral cnt"]  = mon_stat[mon_id]["neutral cnt"] + day_neu
            mon_stat[mon_id]["negative cnt"] = mon_stat[mon_id]["negative cnt"] + day_neg
        else:
            mon_stat[mon_id] = {"positive cnt":0, "neutral cnt":0, "negative cnt":0}
        
        with open(f'./out/{keyword}_stat_day/{y}-{m}-{d}.json', 'w', encoding='utf-8') as f:
            json.dump({"day positive count": day_pos, "day neutral count": day_neu,
                    "day negative count": day_neg, "day distri": pos_dis}, f)

    with open(f'./out/{keyword}_stat_mon.json', 'w', encoding='utf-8') as f:
        json.dump(mon_stat, f)

    hour_list = []
    with open('./data/hour.json', 'r', encoding='utf-8') as f:
        hour_list = json.load(f)
    l = len(hour_list)
    pb = progress_bar(l-1)
    for i in range(l-1):
        y = hour_list[i]['year']
        m = str(int(hour_list[i]['month'])+1)
        d = str(hour_list[i]['day']+1)
        h = hour_list[i]['hour']
        with open(f'./out/{keyword}_hour/{y}-{m}-{d}-{h}.txt', 'r', encoding='utf-8') as f:
            senta.add(f.readlines())
        senta.predict()
        hour_neg = 0
        hour_pos = 0
        hour_neu = 0
        pos_dis = {}
        for item in senta.results:
            positive_prob = round(item['positive_probs'], 2)
            negative_prob = round(item['negative_probs'], 2)
            pos_dis[positive_prob] = pos_dis.get(positive_prob, 0) + 1
            if positive_prob >= 0.85:
                hour_pos += 1
            elif negative_prob >= 0.6:
                hour_neg += 1
            else:
                hour_neu += 1
        with open(f'./out/{keyword}_stat_hour/{y}-{m}-{d}-{h}.json', 'w', encoding='utf-8') as f:
            json.dump({"hour positive count": hour_pos, "hour neutral count": hour_neu,
                    "hour negative count": hour_neg, "hour distri": pos_dis}, f)
        pb.progress(i)

if __name__ == "__main__":
    preprocess("wuhan")
    senti_analysis("wuhan")