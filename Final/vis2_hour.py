import json
from pyecharts.charts import Bar, Pie, Timeline, Grid
from pyecharts.globals import SymbolType, ThemeType
import pyecharts.options as opts

with open('./data/hour.json', 'r', encoding='utf-8') as f:
    hour_list = json.load(f)

tl = Timeline(
    init_opts=opts.InitOpts(width='2200px',
                            height='600px',
                            page_title="武汉微博舆情-分小时",
                            theme=ThemeType.MACARONS)
)
l = len(hour_list)
for i in range(l-1):
    y = hour_list[i]['year']
    m = str(int(hour_list[i]['month'])+1)
    d = str(hour_list[i]['day']+1)
    h = hour_list[i]['hour']
    with open(f'./out/wuhan_stat_hour/{y}-{m}-{d}-{h}.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
        pie = (
            Pie()
            .add(
                series_name="舆情分布",
                data_pair=list(data.items())[:3],
                rosetype="radius",
                radius="55%",
                # center=["50%", "50%"],
                label_opts=opts.LabelOpts(
                    position="outside",
                    formatter="{a|{a}}{abg|}\n{hr|}\n {b|{b}: }{c}  {per|{d}%}  ",
                    background_color="#eee",
                    border_color="#aaa",
                    border_width=1,
                    border_radius=4,
                    rich={
                        "a": {"color": "#999", "lineHeight": 22, "align": "center"},
                        "abg": {
                            "backgroundColor": "#e3e3e3",
                            "width": "100%",
                            "align": "right",
                            "height": 22,
                            "borderRadius": [4, 4, 0, 0],
                        },
                        "hr": {
                            "borderColor": "#aaa",
                            "width": "100%",
                            "borderWidth": 0.5,
                            "height": 0,
                        },
                        "b": {"fontSize": 16, "lineHeight": 33},
                        "per": {
                            "color": "#eee",
                            "backgroundColor": "#334455",
                            "padding": [2, 4],
                            "borderRadius": 2,
                        },
                    },
                )
            )
            .set_global_opts(
                title_opts=opts.TitleOpts(
                    title="Customized Pie",
                    pos_left="center",
                    pos_top="20",
                    title_textstyle_opts=opts.TextStyleOpts(color="#fff"),
                ),
                legend_opts=opts.LegendOpts(is_show=False),
            )
            .set_series_opts(
                tooltip_opts=opts.TooltipOpts(
                    trigger="item", formatter="{a} <br/>{b}: {c} ({d}%)"
                ),
            )
        )
        xdistri = [item[0] for item in sorted(data['hour distri'].items())]
        ydistri = [item[1] for item in sorted(data['hour distri'].items())]
        bar = (
            Bar()
            .add_xaxis(xdistri)
            .add_yaxis('频数', ydistri)
            .set_global_opts(
                title_opts=opts.TitleOpts(title="舆情积极度分布",subtitle=f"{y}年{m}月{d}日-{h}时"),
                yaxis_opts=opts.AxisOpts(name="舆情积极度频数"),
                xaxis_opts=opts.AxisOpts(name="舆情积极度"),
            )
            .set_series_opts(itemstyle_opts = opts.ItemStyleOpts(color="orange"))
        )
    grid = (
        Grid()
        .add(bar, grid_opts=opts.GridOpts(pos_right="65%"))
        .add(pie, grid_opts=opts.GridOpts(pos_left="80%"))
    )
    tl.add(grid, f"{y}-{m}-{d}-{h}")
tl.render('./out/wuhan_byhour.html') 
