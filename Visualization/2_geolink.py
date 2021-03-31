# -*- coding: utf-8 -*-
"""
Created on Mon Mar 16 20:39:22 2020
@author: Justin
"""
from pyecharts import options as opts
from pyecharts.charts import Geo
from pyecharts.faker import Faker
from pyecharts.globals import ChartType, SymbolType

c = (
    Geo()
    .add_schema(
        maptype="陕西",
        itemstyle_opts=opts.ItemStyleOpts(color="lightblue", border_color="black"),
    )
    .add(
        "",
        [("西安", 100), ("汉中", 40), ("榆林", 30), ("延安",50),
         ("安康", 20), ("宝鸡",80), ("铜川", 90), ("咸阳", 70), 
         ("渭南", 60), ("商洛", 10)],
         #城市标记参数是由元组项组成的列表
        type_=ChartType.EFFECT_SCATTER,
        color="white",
    )
    .add(
        "暑假",
        [("汉中", "安康"), ("安康", "商洛"), ("商洛", "西安"), ("西安", "宝鸡"), ("宝鸡", "汉中")],
         #连线方向参数是由元组项组成的列表
        type_=ChartType.LINES,
        effect_opts=opts.EffectOpts(
            symbol=SymbolType.ARROW, symbol_size=6, color="white"
        ),
        linestyle_opts=opts.LineStyleOpts(curve=0.2),
        # curve为正时，曲线是凸的；为负时，曲线是凹的
    )
    .add(
        "寒假（骑行）",
        [("西安", "渭南"), ("渭南", "铜川"), ("铜川", "延安"), ("延安","榆林")],
         #连线方向参数是由元组项组成的列表
        type_=ChartType.LINES,
        effect_opts=opts.EffectOpts(
            symbol=SymbolType.ARROW, symbol_size=6, color="white"
        ),
        linestyle_opts=opts.LineStyleOpts(curve=-0.2),
        # curve为正时，曲线是凸的；为负时，曲线是凹的
    )
    .add(
        "乘火车",
        [("榆林","西安")],
         #连线方向参数是由元组项组成的列表
        type_=ChartType.LINES,
        effect_opts=opts.EffectOpts(
            symbol=SymbolType.ARROW, symbol_size=6, color="white"
        ),
        linestyle_opts=opts.LineStyleOpts(curve=-0.1),
        # curve为正时，曲线是凸的；为负时，曲线是凹的
    )
    .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
    .set_global_opts(
        visualmap_opts=opts.VisualMapOpts(range_color=Faker.visual_color), 
        title_opts=opts.TitleOpts(
            title="省内旅行计划",
            subtitle="骑行或轮滑~"),
        toolbox_opts=opts.ToolboxOpts(),
    )
    .render("./out/geo_shaanxi.html")
)

import os
os.system("start chrome .\out\geo_shaanxi.html")