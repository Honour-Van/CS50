import json
from pyecharts.charts import Bar, Pie, Timeline, Grid
from pyecharts.globals import SymbolType, ThemeType
import pyecharts.options as opts

with open('./data/date.json', 'r', encoding='utf-8') as f:
    date_list = json.load(f)

tl = Timeline(
    init_opts=opts.InitOpts(width='2000px',
                            height='600px',
                            page_title="武汉-微博舆情分日")
)
l = len(date_list)
for i in range(l-1):
    y = date_list[i]['year']
    m = str(int(date_list[i]['month'])+1)
    d = str(date_list[i]['day']+1)
    with open(f'./out/wuhan_stat_day/{y}-{m}-{d}.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
        pie = (
            Pie()
            .add(
                series_name="舆情分布",
                data_pair=list(data.items())[:3],
                rosetype="radius",
                radius="55%",
                center=["50%", "50%"],
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
        xdistri = [item[0] for item in sorted(data['day distri'].items())]
        ydistri = [item[1] for item in sorted(data['day distri'].items())]
        bar = (
            Bar()
            .add_xaxis(xdistri)
            .add_yaxis('频数', ydistri)
            .set_global_opts(
                title_opts=opts.TitleOpts(title="舆情积极度分布"),
                yaxis_opts=opts.AxisOpts(name="舆情积极度频数"),
                xaxis_opts=opts.AxisOpts(name="舆情积极度"),
            )
        )
    grid = Grid()
    grid.add(bar, grid_opts=opts.GridOpts(pos_right="20%"))
    grid.add(pie, grid_opts=opts.GridOpts(pos_left="20%"))
    grid.render()
    tl.add(grid, f"{y}-{m}-{d}")
tl.render('./out/wuhan_byday.html')
