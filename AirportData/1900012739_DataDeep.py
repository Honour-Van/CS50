'''
@file: data_deep.py
@name: 范皓年 1900012739 电子学系
@description: 本文件用于对文件进行分析
'''

#subtask 1：读入数据生成“机场名称+18年吞吐量+17年吞吐量+同比增速”
#       （这个项目里我们规定同比增速=同比增量=增长率）
data = []
with open('./1900012739_cnAirport.txt', 'r', encoding='utf-8') as f:
    f.readline()
    for line in f.readlines():
        content = line.split(',')
        val18 = float(content[2])
        growth = float(content[3])
        if growth == -100:
            continue
        val17 = val18 / (1 + growth/100)
        data.append(tuple([content[1], val18, val17, growth]))
    # print(data)

# substask 2：按17年吞吐量降序
print('\n---------subtask #2: 按照17年吞吐量降序-----------')
data.sort(key=lambda X: X[2], reverse=True)
for i in range(len(data)):
    print(i+1, data[i][0], data[i][1], data[i][2], sep=',')

#subtask 3：按增量降序
print('\n---------subtask #3: 按照吞吐量增量降序-----------')
data.sort(key=lambda X: X[1]-X[2], reverse=True)
for i in range(len(data)):
    print(i+1, data[i][0], data[i][1], data[i][2], sep=',')

#subtask 4: 按增长率降序
print('\n---------subtask #4: 按照吞吐量增长率降序-----------')
data.sort(key=lambda X: X[3], reverse=True)
for i in range(len(data)):
    print(i+1, data[i][0], data[i][1], data[i][2], sep=',')
