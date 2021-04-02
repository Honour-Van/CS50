"""
@file: map.py
@author: 范皓年 1900012739
@description: 
    可视化作业3：地图可视化练习
    我们将GDP数据存入json文件中，随后读取出来，并利用pyecharts相关组件进行地图绘制。

故事背景：
    这个地图主题略微正经，我们将2019年的世界GDP前十作一展示。
    通过GDP Top10和GDPPC(pre capita, 人均国内生产总值)的对比，
    我们可以看出，世界上的GDP大国和GDPPC强国几乎正交。人均GDP高的国家往往是早期的发达国家。
    与之相比，GDP大国往往却出现在当今的发展中国家，以中国为代表的一系列国家，以庞大的人口体量
    带来了经济发展空间。下一个任务我们将基于时间尺度进行。
"""

import os
from pyecharts.faker import Faker
from pyecharts import options as opts
from pyecharts.charts import Map, Page
from pyecharts.globals import ThemeType
import json

from pyecharts.options.charts_options import PageLayoutOpts

# 从json文件导入GDP和GDPPC数据
with open('./assets/GDP.json', 'r', encoding='utf-8') as f:
    gdp_dict = json.load(f)
    gdp_list = [[country[0], country[1]] for country in gdp_dict.items()]
with open('./assets/GDP_ave.json', 'r', encoding='utf-8') as f:
    gdppc_dict = json.load(f)
    gdppc_list = [[country[0], country[1]] for country in gdppc_dict.items()]

# 绘制GDP top10 地图
m1 = (
    Map()
    .add("GDP/$1T",
         gdp_list,
         maptype="world",
         is_map_symbol_show=False,  # 不描点
         )
    .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
    .set_global_opts(
        title_opts=opts.TitleOpts(title="GDP Top10"),
        visualmap_opts=opts.VisualMapOpts(max_=22, is_piecewise=True),
    )
)

# 绘制GDP per capita top10
m2 = (
    Map()
    .add("GDPPC/$10,000",
         gdppc_list,
         maptype="world",
         is_map_symbol_show=False,  # 不描点
         )
    .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
    .set_global_opts(
        title_opts=opts.TitleOpts(title="GDPPC Top10"),
        visualmap_opts=opts.VisualMapOpts(min_=5, max_=12),  # 调整动态范围
    )
)

# 将两个图样放入一个page当中
(
    Page(
        page_title="GDP top10",
    )
    .add(m1, m2)
    .render('./out/map_world_gdp.html')
)

# 尝试直接利用chrome打开html文件
try:
    os.system("start chrome ./out/map_world_gdp.html")
except:
    print("Chrome Error")