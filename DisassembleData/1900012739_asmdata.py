'''
@author: 范皓年 1900012739
@description: 
'''

import pandas as pd
import matplotlib.pyplot as plt

# excelwriter对象生成，用于操作excel表格
writer = pd.ExcelWriter('Instruction_1900012739_.xlsx', engine='xlsxwriter')

# --------任务1：统计指令------------
inst_dict = {} # 统计指令数
with open('./asmData.txt', 'r', encoding='utf-8') as f:
    for line in f.readlines():
        content = line.split()
        if len(content) <= 3:
            continue
        inst_dict[content[3]] = inst_dict.get(content[3], 0) + 1

res1 = sorted(inst_dict.items(), key=lambda x: x[1], reverse=True) # 按指令数量排序

df1 = pd.DataFrame(res1, columns=['Instruction','Count']) # 生成dataframe对象便于操作、写入
df1.to_excel(writer,
             'instructionCount', index=False)

# --------任务2：为任务1添加分类标签------------
param_alia = {4: '无参指令', 5: '单参指令', 6: '双参指令', 7: '多参指令'}
type_dict = {} # 用于统计某个指令的最多参数情况，保持更新使得获得最大参数数量，以求准确
with open('asmData.txt', 'r', encoding='utf-8') as f:
    for line in f.readlines():
        content = line.split()
        if content[-1] == 'return;':
            content = content[:-1]
        l = len(content)
        if l <= 3:
            continue
        elif l > 7:
            l = 7
        type_dict[content[3]] = max([type_dict.get(content[3], 0), l])

# 按照1中的顺序生成一个指令种类统计
res2 = []
for item in res1:
    res2.append([item[0], param_alia[type_dict[item[0]]]])
df2 = pd.DataFrame(res2, columns=['Instruction', 'Type'])
df2.to_excel(writer,
             'instructionType', index=False)

# --------任务3：汇总1和2------------

df3 = df2
# 汇总
df3.insert(1, 'Amount', [inst_dict[x] for x in df2.iloc[:, 0]])
df3.to_excel(writer, 'Summary', index=False)

# -----------任务4：按类统计------------------
param_dict = {} # 统计每个类之下有多少个指令
for item in res2:
    param_dict[item[1]] = param_dict.get(item[1], 0) + inst_dict[item[0]]

res4 = sorted(param_dict.items(), key=lambda x: x[1], reverse=True)
df4 = pd.DataFrame(res4, columns=['Type', 'Amount'])

inst_dict4 = {}  # 每个类之下有多少种指令
for item in type_dict.keys():
    tp = param_alia[type_dict[item]]
    inst_dict4[tp] = inst_dict4.get(tp, 0) + 1

df4.insert(1, 'Numbers', [inst_dict4[x] for x in df4.iloc[:, 0]])
print(df4)

# 准备绘图
plt.rcParams['font.sans-serif'] = ['KaiTi'] # 指定默认字体
plt.rcParams['axes.unicode_minus'] = False # 解决保存图像是负号'-'显示为方块的问题
# 绘图
fig = plt.figure()
ax1 = fig.add_subplot(2, 1, 1) # 添加子图
ax1.set_title('指令种类数') # 设置子图名称
plt.bar(df4.iloc[:,0], df4.iloc[:,1]) #绘图
ax2 = fig.add_subplot(2, 1, 2)
ax2.set_title('指令总数')
plt.bar(df4.iloc[:,0], df4.iloc[:,2])
plt.title('指令数统计')
plt.tight_layout() # 调整图片元素分布
# plt.show() # 如果这一句显示，则图片为空白
plt.savefig('./foo.png')
writer.book.add_worksheet('Chart').insert_image(0,0,'./foo.png') # 保存图片

# -----------保存退出------------------
writer.save() # 写入excel表格
