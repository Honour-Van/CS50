from pyecharts.charts import WordCloud
from pyecharts.charts.basic_charts.wordcloud import gen_color
from pyecharts.charts import Bar
from pyecharts.charts import PictorialBar
from pyecharts.globals import SymbolType
import pyecharts.options as opts

# -------从文件中读出人物词频------------------
src_filename = './assets/红楼梦词频.csv'
# 格式：人物,出现次数

with open(src_filename, 'r', encoding='utf-8') as src_file:
    line_list = src_file.readlines()  # 返回列表，文件中的一行是一个元素

# print(line_list)  # 检查读入数据的情况

# 将读入的每行数据拆分成元组
wordfreq_list = []  # 用于保存元组(人物姓名,出现次数)
for line in line_list:
    line = line.strip()  # 删除'\n'
    line_split = line.split(',')  # 以逗号作为标志，把字符串切分成词，存在列表中
    wordfreq_list.append((line_split[0], line_split[1]))

# print(wordfreq_list)

del wordfreq_list[0]  # 删除csv文件中的标题行
# -------从文件中读出人物词频完成------------------

# -------绘制词频的词云图----------------------
(
    WordCloud()
    .add(series_name="词频分析", 
        data_pair=wordfreq_list[:100], 
        word_size_range=[6, 66], 
        shape='roundRect',
        height=800,
        width=1200,
        pos_left=0
        )
    .set_global_opts(
        title_opts=opts.TitleOpts(
            title="词频分析",
            subtitle="以红楼梦为例", 
            title_textstyle_opts=opts.TextStyleOpts(font_size=23)
        ),
        tooltip_opts=opts.TooltipOpts(is_show=True),
    )
    .render("./out/wordcloud.html")
)

# --------绘制词云图完成----------------------

# -------绘制词频的柱形图----------------------
xdata = [x[0] for x in wordfreq_list[:10]]
ydata = [y[1] for y in wordfreq_list[:10]]
(
    Bar()
    .add_xaxis(xdata)
    .add_yaxis("词频", ydata, color='darkblue')
    .set_global_opts(
        title_opts=opts.TitleOpts(
            title="词频统计", 
            subtitle="以红楼梦为例")
    )
    .render('./out/bar.html')
)

# --------绘制柱形图完成----------------------


(
    PictorialBar()
    .add_xaxis(xdata)
    .add_yaxis(
        "",
        ydata,
        label_opts=opts.LabelOpts(is_show=False),
        symbol_size=18,
        symbol_repeat="fixed",
        symbol_offset=[0, 0],
        is_symbol_clip=True,
        symbol=SymbolType.ROUND_RECT,
        color='darkblue'
    )
    .reversal_axis()
    .set_global_opts(
        title_opts=opts.TitleOpts(
            title="词频象形柱图",
            subtitle="以红楼梦为例"
        ),
        xaxis_opts=opts.AxisOpts(is_show=False),
        yaxis_opts=opts.AxisOpts(
            axistick_opts=opts.AxisTickOpts(is_show=False),
            axisline_opts=opts.AxisLineOpts(
                linestyle_opts=opts.LineStyleOpts(opacity=0)
            ),
        ),
    )
    .render("./out/pictorialbar.html")
)


import os
try:
    os.system('start chrome ./out/wordcloud.html')
    os.system('start chrome ./out/bar.html')
    os.system('start chrome ./out/pictorialbar.html')
except:
    print("Chrome Open Error")