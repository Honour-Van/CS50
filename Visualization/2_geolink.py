"""
@file: geolink.py
@author: 范皓年 1900012739
@description: 
    可视化作业2：地理坐标系图练习
    利用pyecharts实现地图以及连线。
    这个地图使用地理散点和连线两种基本图样描述了寒暑假旅行示意图
故事背景：
    一个漫长的寒假，内卷自学新知识累的半死的小h想在省内走一走，
    从西安出发，ta本来想沿着全省来一次环省旅行，但是发现越往北走，气候越不好，所以ta打算尽可能往南走
    骑车或者轮滑都令人困倦。由于他的精力是有限的，他必须要用最低的成本走完越多的路程。
    每一条路径的消耗都已经以list的形式给出，没有在图中给出。在一定的城市可以获得一定的补充。
    由于你刚刚学会python，尝试编写一个程序帮他找到最佳的路径遍历陕南。注意：Floyd算法可能会超时。
    （手动狗头：这个程序和算法题毫无关联
"""

import os
from pyecharts import options as opts
from pyecharts.charts import Geo
from pyecharts.faker import Faker
from pyecharts.globals import ChartType, SymbolType, ThemeType

# 地理图的链式调用
(
    Geo(
        init_opts=opts.InitOpts(
            theme=ThemeType.INFOGRAPHIC,
            bg_color='white',
            page_title='Honour的省内旅行路线'
        )
    ) # 确定主题、标签页名称等
    .add_schema(
        maptype="陕西",
        itemstyle_opts=opts.ItemStyleOpts(
            color="lightblue", border_color="black"),
    ) # 确定地图基本属性
    .add(
        "",
        [("西安", 100), ("汉中", 40), ("榆林", 30), ("延安", 50),
         ("安康", 20), ("宝鸡", 80), ("铜川", 90), ("咸阳", 70),
         ("渭南", 60), ("商洛", 10)],
        # 城市标记参数是由元组项组成的列表
        type_=ChartType.EFFECT_SCATTER,
        color="white",
    ) # 在省内各城市加点，按照产值排序
    .add(
        "暑假",
        [("汉中", "安康"), ("安康", "商洛"), ("商洛", "西安"), ("西安", "宝鸡"), ("宝鸡", "汉中")],
        # 连线方向参数是由元组项组成的列表
        type_=ChartType.LINES,
        effect_opts=opts.EffectOpts(
            symbol=SymbolType.ARROW, symbol_size=6, color="white"
        ),
        linestyle_opts=opts.LineStyleOpts(curve=0.2),
        # curve为正时，曲线是凸的；为负时，曲线是凹的
    )
    .add(
        "寒假（骑行）",
        [("西安", "渭南"), ("渭南", "铜川"), ("铜川", "延安"), ("延安", "榆林")],
        # 连线方向参数是由元组项组成的列表
        type_=ChartType.LINES,
        effect_opts=opts.EffectOpts(
            symbol=SymbolType.ARROW, symbol_size=6, color="white"
        ),
        linestyle_opts=opts.LineStyleOpts(curve=-0.2),
        # curve为正时，曲线是凸的；为负时，曲线是凹的
    )
    .add(
        "乘火车",
        [("榆林", "西安")],
        # 连线方向参数是由元组项组成的列表
        type_=ChartType.LINES,
        effect_opts=opts.EffectOpts(
            symbol=SymbolType.TRIANGLE, symbol_size=6, color="white"
        ),
        linestyle_opts=opts.LineStyleOpts(curve=-0.1),
        # curve为正时，曲线是凸的；为负时，曲线是凹的
    )
    .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
    .set_global_opts(
        visualmap_opts=opts.VisualMapOpts(range_color=Faker.visual_color),
        title_opts=opts.TitleOpts(
            title="省内旅行计划",
            subtitle="骑行或轮滑"),
        toolbox_opts=opts.ToolboxOpts(),
    )
    .render("./out/geo_shaanxi.html")
)

# 尝试直接利用chrome打开html文件
try:
    os.system("start chrome .\out\geo_shaanxi.html")
except:
    print("Chrome Error")