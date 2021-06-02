import json
# 用于生成2019年的所有日期的字典
hour_list = []
date_list = []
for i in range(31):
    date_list.append({'year':'2019', 'month':'11', 'day':i})
    for j in range(24):
        hour_list.append({'year':'2019', 'month':'11', 'day':i, 'hour':str(j)})
for i in range(12):
    monthday = 31
    if i == 2-1:
        monthday = 29
    elif i == 4-1 or i == 6-1 or i == 9-1 or i == 11-1:
        monthday = 30
    for j in range(monthday):
        date_list.append({'year':'2020','month':str(i), 'day':j})
        for k in range(24):
            hour_list.append({'year':'2020', 'month':str(i), 'day':j, 'hour':str(k)})

with open("./data/hour.json", 'w', encoding='utf-8') as hour_file:
    json.dump(hour_list, hour_file)

with open("./data/date.json", 'w', encoding='utf-8') as date_file:
    json.dump(date_list, date_file)
