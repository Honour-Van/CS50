from pyecharts import options as opts
from pyecharts.charts import Bar, Grid, Line, Scatter
import json

with open("./assets/GDP.json", 'r', encoding='utf-8') as f:
    gdp_dict = json.load(f)
    x_data = list(gdp_dict.keys())
    y1_data= list(gdp_dict.values())
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
            max_=100,
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
    # .extend_axis(
    #     yaxis=opts.AxisOpts(
    #         name="2020",
    #         type_="value",
    #         min_=0,
    #         max_=22,
    #         position="right",
    #         offset=60,
    #         axisline_opts=opts.AxisLineOpts(
    #             linestyle_opts=opts.LineStyleOpts(color="#d14a61")
    #         ),
    #         axislabel_opts=opts.LabelOpts(
    #             formatter="${value}"
    #         ),
    #     )
    # )
    .set_global_opts(
        yaxis_opts=opts.AxisOpts(
            name="GDP",
            min_=0,
            max_=22,
            position="right",
            offset=0,#Y 轴相对于默认位置的偏移，在相同的 position 上有多个 Y 轴的时候有用
            axisline_opts=opts.AxisLineOpts(
                linestyle_opts=opts.LineStyleOpts(color="#675bba")
            ),
            axislabel_opts={
                "formatter":"${value} trillion",
                "rotate":-10,
            }
        ),
        xaxis_opts=opts.AxisOpts(
            # name="country",
            axislabel_opts={"rotate":30}
        ),
        title_opts=opts.TitleOpts(title="GDP Top10"),
        tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type="cross"),#提示框配置项
    )
)

bar.render('./out/grid_mult_yaxis.html')

from os import system
system("start chrome ./out/grid_mult_yaxis.html")