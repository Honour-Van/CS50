'''
@author: 范皓年 1900012739
@description: 
'''

from numpy.core.fromnumeric import sort
import pandas as pd
import matplotlib.pyplot as plt
import xlsxwriter

# --------任务1：统计指令------------
inst_dict = {}
with open('./asmData.txt', 'r', encoding='utf-8') as f:
    for line in f.readlines():
        content = line.split()
        if len(content) <= 3:
            continue
        inst_dict[content[3]] = inst_dict.get(content[3], 0) + 1

res1 = sorted(inst_dict.items(), key=lambda x: x[1], reverse=True)
with open('./stat.txt', 'w', encoding='utf-8') as fw:
    for item in res1:
        fw.write(item[0] + ' ' + str(item[1]) + '\n')

writer = pd.ExcelWriter('Instruction_1900012739_.xlsx', engine='xlsxwriter')
df1 = pd.DataFrame(res1)
df1.to_excel(writer,
             'instructionCount', index=False, header=None)

# --------任务2：指令参数------------
param_dict = {}
param_alia = {4: '无参指令', 5: '单参指令', 6: '双参指令', 7: '多参指令'}
with open('./asmData.txt', 'r', encoding='utf-8') as f:
    for line in f.readlines():
        content = line.split()
        if content[-1] == 'return;':
            content = content[:-1]
        l = len(content)
        if l <= 3:
            continue
        elif l > 7:
            l = 7
        param_dict[param_alia[l]] = param_dict.get(param_alia[l], 0) + 1

res2 = sorted(param_dict.items(), key=lambda x: x[1], reverse=True)
df2 = pd.DataFrame(res2, columns=['指令类型', '指令总量'])
df2.to_excel(writer,
             'instructionType', index=False, header=None)

# --------任务3：为任务1添加分类标签------------
type_dict = {}
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

res3 = []
for item in res1:
    res3.append([item[0], item[1], param_alia[type_dict[item[0]]]])
df3 = pd.DataFrame(res3)
df3.to_excel(writer, 'Summary', index=False, header=None)

# -----------任务4：绘制图片------------------
inst_dict4 = {}  # 每个类之下有多少种指令
for item in type_dict.keys():
    tp = param_alia[type_dict[item]]
    inst_dict4[tp] = inst_dict4.get(tp, 0) + 1

df4 = df2
df4.insert(1, '指令种类数', [inst_dict4[x] for x in df4.iloc[:, 0]])
print(df4)

plt.rcParams['font.sans-serif'] = ['KaiTi'] # 指定默认字体
plt.rcParams['axes.unicode_minus'] = False # 解决保存图像是负号'-'显示为方块的问题
fig = plt.figure()
ax1 = fig.add_subplot(2, 1, 1)
ax1.set_title('指令种类数')
plt.bar(df4.iloc[:,0], df4.iloc[:,1])
ax2 = fig.add_subplot(2, 1, 2)
ax2.set_title('指令总数')
plt.bar(df4.iloc[:,0], df4.iloc[:,2])
plt.title('指令数统计')
plt.tight_layout()
# plt.show()
plt.savefig('./foo.png')
writer.book.add_worksheet('Chart').insert_image(0,0,'./foo.png')

# -----------保存退出------------------
writer.save()
