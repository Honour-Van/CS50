"""
@file: wordfreq.py
@author: 范皓年 1900012739
@description: 
    可视化作业1：利用三种图形进行词频可视化
    基于之前在文本分析中得到的结果，
    我们这里利用柱形图、词云图和象形柱状图进行数据可视化
"""

from pyecharts.charts import WordCloud, Bar, PictorialBar, Tab
from pyecharts.globals import SymbolType, ThemeType
import pyecharts.options as opts
import os

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

# print(wordfreq_list)  # 检查读入数据的情况

del wordfreq_list[0]  # 删除csv文件中的标题行
# -------从文件中读出人物词频完成------------------

# -------绘制词频的词云图----------------------
wordcloud = (
    WordCloud(
        init_opts=opts.InitOpts(
            theme=ThemeType.INFOGRAPHIC,
            page_title='红楼梦词云'
        )
    )
    .add(series_name="词频分析",
         data_pair=wordfreq_list[:200],
         word_size_range=[6, 66],
         shape='roundRect',

         )
    .set_global_opts(
        title_opts=opts.TitleOpts(
            title="词频分析",
            subtitle="以红楼梦为例",
            title_textstyle_opts=opts.TextStyleOpts(font_size=23)
        ),
        tooltip_opts=opts.TooltipOpts(is_show=True),
        toolbox_opts=opts.ToolboxOpts()
    )
)

# --------绘制词云图完成----------------------

# -------绘制词频的柱形图----------------------
xdata = [x[0] for x in wordfreq_list[:16]]
ydata = [y[1] for y in wordfreq_list[:16]]
bar = (
    Bar(
        init_opts=opts.InitOpts(
            theme=ThemeType.DARK
        )
    )
    .add_xaxis(xdata)
    .add_yaxis("词频", ydata, color='darkblue')
    .set_global_opts(
        title_opts=opts.TitleOpts(
            title="词频统计",
            subtitle="以红楼梦为例"),
        toolbox_opts=opts.ToolboxOpts(),
        xaxis_opts=opts.AxisOpts(
            # is_show=False,
            axislabel_opts={"rotate":45}
        ),
    )
)

# --------绘制柱形图完成----------------------

# --------绘制象形柱状图----------------------
pictorialbar = (
    PictorialBar(
        init_opts=opts.InitOpts(
            theme=ThemeType.WONDERLAND,
            page_title='红楼梦词频象形柱状图'
        )
    )
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
        yaxis_opts=opts.AxisOpts(
            axistick_opts=opts.AxisTickOpts(is_show=False),
            axisline_opts=opts.AxisLineOpts(
                linestyle_opts=opts.LineStyleOpts(opacity=0)
            ),
        ),
        toolbox_opts=opts.ToolboxOpts(),
    )
)
# --------象形柱形图完成----------------------

# --------将几个图片绘制到同一个tab中---------
(
    Tab(page_title='红楼梦词频分析')
    .add(bar, "词频柱形图")
    .add(wordcloud, "词云图")
    .add(pictorialbar, "象形柱状图")
    .render('./out/wordfreq.html')
)
# --------tab绘制完成-----------------------

# 尝试直接利用chrome打开html文件
try:
    os.system('start chrome ./out/wordfreq.html')
except:
    print("Chrome Error")