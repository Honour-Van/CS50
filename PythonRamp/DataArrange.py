'''
@file: data_arrange.py
@name: 范皓年 北大EE
@description: 本文件用于初步清洗数据
'''
with open('./ChinaAirportData.txt', 'r', encoding='utf-8') as f:
    with open('./cnAirport.txt', 'w', encoding='utf-8') as fw:
        fw.write(f.readline())
    for line in f.readlines():
        content = line.split(',')
        if len(content[2]) == 0:
            continue
        resline = content[0] + ',' + content[1] + ','
        for piece in content[2:-1]:
            resline += piece
        resline =  resline + ',' + content[-1]
        with open('./cnAirport.txt', 'a', encoding='utf-8') as fw:
            fw.write(resline) 