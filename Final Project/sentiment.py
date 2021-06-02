from senta import Senta

import json
from mytool import progress_bar
date_list = []
with open('./data/date.json', 'r', encoding='utf-8') as f:
    date_list = json.load(f)
l = len(date_list)

senta = Senta()
# pb = progress_bar(l)

# mon_stat = {}
# for i in range(l-1):
#     y = date_list[i]['year']
#     m = str(int(date_list[i]['month'])+1)
#     d = str(date_list[i]['day']+1)
#     pb.progress(i)

#     with open(f'./out/wuhan_day/{y}-{m}-{d}.txt', 'r', encoding='utf-8') as f:
#         senta.add(f.readlines())
#     senta.predict()
#     day_sum = 0
#     day_pos = 0
#     day_neu = 0
#     pos_dis = {}
#     for item in senta.results:
#         day_sum += 1
#         positive_prob = round(item['positive_probs'], 2)
#         negative_prob = round(item['negative_probs'], 2)
#         pos_dis[positive_prob] = pos_dis.get(positive_prob, 0) + 1
#         if positive_prob >= 0.6:
#             day_pos += 1
#         elif positive_prob >= 0.4:
#             day_neu += 1
#     mon_id = f"{y}-{m}"
#     if mon_id in mon_stat:
#         mon_stat[mon_id]["positive cnt"] = mon_stat[mon_id]["positive cnt"] + day_pos
#         mon_stat[mon_id]["neutral cnt"]  = mon_stat[mon_id]["neutral cnt"] + day_neu
#         mon_stat[mon_id]["negative cnt"] = mon_stat[mon_id]["negative cnt"] + day_sum - day_neu - day_pos
#     else:
#         mon_stat[mon_id] = {"positive cnt":0, "neutral cnt":0, "negative cnt":0}
    
#     pos_rate = round(day_pos/day_sum, 2)
#     neu_rate = round(day_neu/day_sum, 2)
#     with open(f'./out/wuhan_stat_day/{y}-{m}-{d}.json', 'w', encoding='utf-8') as f:
#         json.dump({"day positive rate": pos_rate, "day neutral rate": neu_rate,
#                   "day negative rate": round(1-pos_rate-neu_rate, 2), "day distri": pos_dis}, f)

# with open('./out/wuhan_stat_mon.json', 'w', encoding='utf-8') as f:
#     json.dump(mon_stat, f)

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
    with open(f'./out/wuhan_raw/{y}-{m}-{d}-{h}.txt', 'r', encoding='utf-8') as f:
        senta.add(f.readlines())
    senta.predict()
    hour_sum = 0
    hour_pos = 0
    hour_neu = 0
    pos_dis = {}
    for item in senta.results:
        hour_sum += 1
        positive_prob = round(item['positive_probs'], 2)
        negative_prob = round(item['negative_probs'], 2)
        pos_dis[positive_prob] = pos_dis.get(positive_prob, 0) + 1
        if positive_prob >= 0.6:
            hour_pos += 1
        elif positive_prob >= 0.4:
            hour_neu += 1
    if hour_sum == 0:
        continue
    pos_rate = round(hour_pos/hour_sum, 2)
    neu_rate = round(hour_neu/hour_sum, 2)
    with open(f'./out/wuhan_stat_hour/{y}-{m}-{d}-{h}.json', 'w', encoding='utf-8') as f:
        json.dump({"hour positive rate": pos_rate, "hour neutral rate": neu_rate,
                  "hour negative rate": round(1-pos_rate-neu_rate, 2), "hour distri": pos_dis}, f)
    pb.progress(i)