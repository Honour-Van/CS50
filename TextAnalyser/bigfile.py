import jieba
from wordcloud import WordCloud
import matplotlib.pyplot as plt

txt_filename = './raw2.txt'
result_filename = './output2.csv'

ignore_list = []
cloud_material = ""
word_dict = {}

# 从文件读取文本
with open(txt_filename, 'r', encoding='utf-8') as f:
    for line in f:
        # 分词
        word_list = jieba.lcut(line)

        # 用字典统计每个词的出现次数
        for w in word_list:
            # 跳过单字
            if len(w) == 1:
                continue

            # 跳过不想统计的词
            if w in ignore_list:
                continue

            # 对指代同一人物的名词进行合并
            if w == '孔明':
                w = '诸葛亮'
            elif w == '玄德' or w == '刘玄德':
                w = '刘备'
            elif w == '云长' or w == '关公':
                w = '关羽'
            elif w == '后主':
                w = '刘禅'
            else:
                pass  # pass表示“什么都不做”，常用于为尚未完成的代码占位置

            # 已在字典中的词，将出现次数增加1；否则，添加进字典，次数记为1
            if w in word_dict.keys():
                word_dict[w] = word_dict[w] + 1
            else:
                word_dict[w] = 1

            cloud_material = cloud_material + " " + w

wordcloud = WordCloud(
    # 生成中文字的字体,必须要加,不然看不到中文
    font_path="C:\Windows\Fonts\simhei.ttf"
).generate(cloud_material)
image_produce = wordcloud.to_image()
fig = plt.figure(1)
plt.imshow(image_produce)
plt.axis('off')
# plt.show() # 如果加这一句那么不能存图片

plt.gca().xaxis.set_major_locator(plt.NullLocator())
plt.gca().yaxis.set_major_locator(plt.NullLocator())
plt.subplots_adjust(top = 1, bottom = 0, right = 1, left = 0, hspace = 0, wspace = 0)
plt.margins(0,0)
plt.savefig('./wordcloud2.png', box_inches='tight')

# 把字典转成列表，并按原先“键值对”中的“值”从大到小排序
items_list = list(word_dict.items())
items_list.sort(key=lambda x: x[1], reverse=True)

total_num = len(items_list)
print('经统计，共有' + str(total_num) + '个不同的词')

# 根据用户需求，打印排名前列的词，同时把统计结果存入文件
num = input('您想查看前多少个人物？[10]:')
if not num.isdigit() or num == '':  # 如果输入的不全是数字，或者直接按了回车
    num = 10  # 设成查看前10名
else:
    num = int(num)  # 如果输入了正常的数字，则按用户需求设置

result_file = open(result_filename, 'w')   # 新建结果文件

result_file.write('人物,出现次数\n')  # 写入标题行

for i in range(num):
    word, cnt = items_list[i]
    message = str(i+1) + '. ' + word + '\t' + str(cnt)
    print(message)
    result_file.write(word + ',' + str(cnt) + '\n')

result_file.close()  # 关闭文件

print('已写入文件：' + result_filename)
