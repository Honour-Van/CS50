from os import name, system
from pyecharts import options as opts
from pyecharts.charts.chart import Chart
from pyecharts.globals import ChartType, SymbolType
from pyecharts.charts import Bar, EffectScatter, Page, Geo, Tab
import json

with open("./assets/GDP.json", 'r', encoding='utf-8') as f:
    gdp_dict = json.load(f)
    x_data = list(gdp_dict.keys())
    y1_data = list(gdp_dict.values())
with open("./assets/GDP_2020.json", 'r', encoding='utf-8') as f:
    gdp_dict = json.load(f)
    y2_data = list(gdp_dict.values())

bar = (
    Bar()
    .add_xaxis(
        x_data,
    )
    .add_yaxis(
        "GDP Top10 in 2019",
        y1_data,
        itemstyle_opts=opts.ItemStyleOpts(color='#5793ff'),
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
        symbol=SymbolType.DIAMOND
    )
)

bar.overlap(c)


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

system("start chrome ./out/pandemic-gdp.html")
