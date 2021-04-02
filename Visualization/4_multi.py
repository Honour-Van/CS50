"""
@file: multi.py
@author: 范皓年 1900012739
@description: 
    可视化作业4：组合图表练习
    我们将GDP数据存入json文件中，随后读取出来，并利用pyecharts相关组件进行地图绘制。

故事背景：
    这个在任务3的基础上加入了时间的考虑，但由于我们选取的事件是疫情相关，
    所以时间线并不长，所以我们没有使用timeline结构。

    我们选取了两个主题进行分析，一个是疫情的感染率，来表征一个国家受到疫情的冲击程度。
    另一方面我们选用了GDP的减量进行展示。两相对比，我们发现，除美国外，其他国家大都有如下的特征：
    1. 一类国家采用对疫情的强硬措施，以中国为代表，采用了相对强的休克性疗法，这样的结果是，有效地控制疫情，但是GDP减量较大
    2. 一类国家采用保持经济的措施，以欧洲部分国家家为代表，一定程度上保持了经济稳定运行，但是不强力阻滞疫情发展，导致了较为严重的疫情
    从这个比较当中我们不难看出中国为了保障人民的生命健康权益，所做出的重大牺牲。
"""

from os import name, system
from pyecharts import options as opts
from pyecharts.charts.chart import Chart
from pyecharts.globals import ChartType, SymbolType
from pyecharts.charts import Bar, EffectScatter, Page, Geo, Tab
import json

# --------------------导入GDP和疫情数据----------------
with open("./assets/GDP.json", 'r', encoding='utf-8') as f:
    gdp_dict = json.load(f)
    x_data = list(gdp_dict.keys())
    y1_data = list(gdp_dict.values())
with open("./assets/GDP_2020.json", 'r', encoding='utf-8') as f:
    gdp_dict = json.load(f)
    y2_data = list(gdp_dict.values())
# -------------------------------------------------------



# ==================制作柱形和涟漪散点图的overlap图式============
# -------------------生成并列柱形图--------------------------
bar = (
    Bar()
    .add_xaxis(
        x_data,
    )
    .add_yaxis(
        "GDP Top10 in 2019",
        y1_data,
        itemstyle_opts=opts.ItemStyleOpts(color='#5793ff'), #注意这里要用ItemStyleOpts
        yaxis_index=0,
    )
    .add_yaxis(
        "GDP Top10 in 2020",
        y2_data,
        yaxis_index=0,
        itemstyle_opts=opts.ItemStyleOpts(color='#d14a61'),
    )
    .extend_axis(
        yaxis=opts.AxisOpts(
            type_="value",
            name="COVID-19 rate",
            min_=0,
            max_=10,
            position="left",
            axisline_opts=opts.AxisLineOpts(
                linestyle_opts=opts.LineStyleOpts(color="#3ba25f")
            ),
            axislabel_opts=opts.LabelOpts(formatter="{value}%"),
            splitline_opts=opts.SplitLineOpts(
                is_show=True, linestyle_opts=opts.LineStyleOpts(opacity=1)
            ),
        )
    )
    .set_global_opts(
        yaxis_opts=opts.AxisOpts(
            name="GDP",
            min_=0,
            max_=22,
            position="right",
            offset=0,  # Y 轴相对于默认位置的偏移，在相同的 position 上有多个 Y 轴的时候有用
            axisline_opts=opts.AxisLineOpts(
                linestyle_opts=opts.LineStyleOpts(color="#675bba")
            ),
            axislabel_opts={
                "formatter": "${value} trillion",
                "rotate": -10,
            }
        ),
        xaxis_opts=opts.AxisOpts(
            # name="country",
            axislabel_opts={"rotate": 30}
        ),
        title_opts=opts.TitleOpts(title="GDP Top10"),
        tooltip_opts=opts.TooltipOpts(
            trigger="axis", axis_pointer_type="cross"),  # 提示框配置项
    )
)

# -----------------生成涟漪散点图---------------------------------------
with open("./assets/pandemic.json", 'r', encoding='utf-8') as f:
    cvd_dict = json.load(f)
    y3_data = [("%.1f"%(100*x['confirmed']/x['population'])) for x in cvd_dict.values()]
c = (
    EffectScatter()
    .add_xaxis(
        x_data,
    )
    .add_yaxis(
        "COVID-19 rate",
        y3_data,
        yaxis_index=1,
        itemstyle_opts=opts.ItemStyleOpts(color='#3ba25f'),
        symbol=SymbolType.DIAMOND # 更换特效类型
    )
)

bar.overlap(c) # 进行图片堆叠

# ===========================GDP和疫情状况图表完成====================

# =========================构建直观的地图展示========================
y4_data = [list((x[0], ("%1.f"%((float(x[1])-float(x[2]))*45+5)))) for x in zip(x_data, y1_data, y2_data)]
geo = (
    Geo()
    .add_schema(maptype='world')
    .add_coordinate_json(json_file='./assets/world_country.json')
    .add(
        "GDP decrement",
        y4_data,
        type_=ChartType.EFFECT_SCATTER,
        is_selected=False,
        symbol=SymbolType.ROUND_RECT
    )
    .add(
        "Pandemic",
        [list((x[0], ("%.1f"%(100*10*x[1]['confirmed']/x[1]['population'])))) for x in cvd_dict.items()], 
        type_=ChartType.EFFECT_SCATTER,
        symbol=SymbolType.DIAMOND
    )
    .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
    .set_global_opts(
        visualmap_opts=opts.VisualMapOpts(),
        title_opts=opts.TitleOpts(title="GDP decrement in these countries"),
    )
)
# =========================地图展示完成========================

# =======================图片组合=============================
page = (
    Page(
        page_title = "COVID-19 effecting GDP Top10",
        layout=Page.SimplePageLayout
    )
    .add(
        bar,
        geo,
    )
    .render("./out/pandemic-gdp.html")
)

# 尝试直接利用chrome打开html文件
try:
    system("start chrome ./out/pandemic-gdp.html")
except:
    print("Chrome Error")
