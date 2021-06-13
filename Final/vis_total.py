import json
from pyecharts.charts import Bar, Pie, Timeline, Grid, Page
from pyecharts.globals import ThemeType
import pyecharts.options as opts

page = Page(page_title="武汉微博舆情")

# vis1
with open('./data/date.json', 'r', encoding='utf-8') as f:
    date_list = json.load(f)

tl = Timeline(
    init_opts=opts.InitOpts(width='1700px',
                            height='600px',
                            page_title="武汉微博舆情-分日",
                            theme=ThemeType.MACARONS)
)
# l = len(date_list)
l = 80
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
                title_opts=opts.TitleOpts(title="舆情积极度分布",subtitle=f"{y}年{m}月{d}日"),
                yaxis_opts=opts.AxisOpts(name="舆情积极度频数"),
                xaxis_opts=opts.AxisOpts(name="舆情积极度"),
            )
            .set_series_opts(itemstyle_opts = opts.ItemStyleOpts(color="orange"))
        )
    grid = (
        Grid()
        .add(bar, grid_opts=opts.GridOpts(pos_right="20%"))
        .add(pie, grid_opts=opts.GridOpts(pos_left="20%"))
    )
    tl.add(grid, f"{y}-{m}-{d}")
page.add(tl)


# vis2
with open('./data/hour.json', 'r', encoding='utf-8') as f:
    hour_list = json.load(f)

tl = Timeline(
    init_opts=opts.InitOpts(width='2200px',
                            height='600px',
                            page_title="武汉微博舆情-分小时",
                            theme=ThemeType.MACARONS)
)
# l = len(hour_list)
l = 300
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
page.add(tl)

# vis3
with open('./out/wuhan_stat_mon.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
bar = (
    Bar()
    .add_xaxis(list(data.keys()))
    .add_yaxis("positive count", [(item[1]['positive cnt']/(item[1]['positive cnt']+item[1]['neutral cnt']+item[1]['negative cnt'])) for item in data.items()], stack='stack1')
    .add_yaxis("neutral count", [(item[1]['neutral cnt']/(item[1]['positive cnt']+item[1]['neutral cnt']+item[1]['negative cnt'])) for item in data.items()], stack='stack1')
    .add_yaxis("negative count", [item[1]['negative cnt']/(item[1]['positive cnt']+item[1]['neutral cnt']+item[1]['negative cnt']) for item in data.items()], stack='stack1')
    .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
    .set_global_opts(title_opts=opts.TitleOpts(title="武汉微博舆情-按月"),datazoom_opts=opts.DataZoomOpts())
)
page.add(bar)

# vis4
l = len(date_list)
day_pos = []
day_neu = []
day_neg = []
day_name = []
for i in range(l-1):
    y = date_list[i]['year']
    m = str(int(date_list[i]['month'])+1)
    d = str(date_list[i]['day']+1)
    with open(f'./out/wuhan_stat_day/{y}-{m}-{d}.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
        tmp_pos = data["day positive count"]
        tmp_neu = data["day neutral count"]
        tmp_neg = data["day negative count"]
        day_name.append(f"{y}-{m}-{d}")
        tmp_sum = tmp_pos + tmp_neu + tmp_neg
        day_pos.append(tmp_pos / tmp_sum)
        day_neu.append(tmp_neu / tmp_sum)
        day_neg.append(tmp_neg / tmp_sum)

bar = (
    Bar(init_opts=opts.InitOpts(width='1700px',
                            height='600px',
                            page_title="武汉微博舆情-分日折线图",
                            theme=ThemeType.INFOGRAPHIC))
    .add_xaxis(day_name)
    .add_yaxis("positive count", day_pos, stack='stack1')
    .add_yaxis("neutral count", day_neu, stack='stack1')
    .add_yaxis("negative count", day_neg, stack='stack1')
    .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
    .set_global_opts(title_opts=opts.TitleOpts(title="武汉微博舆情-分日"),datazoom_opts=opts.DataZoomOpts())
)
page.add(bar)

# vis5
tl = Timeline(
    init_opts=opts.InitOpts(width='1400px',
                            height='1000px',
                            page_title="微博热榜",
                            theme=ThemeType.INFOGRAPHIC)
)
with open('./out/hotrank_stat.json') as f:
    sentidata = json.load(f)
import os
for root, dirs, files in os.walk('./out/hotrank/'):
    cnt = 0
    for file in files[:100]:
        xdata = []
        ydata = []
        with open(root+file,'r', encoding='utf-8') as f:
            for line in f.readlines():
                xdata.append(line.split(',')[0])
                ydata.append(line.split(',')[1])
        rank = (
            Bar()
            .add_xaxis(xdata[::-1])
            .add_yaxis('热度',ydata[::-1])
            .reversal_axis()
            .set_global_opts(
                title_opts=opts.TitleOpts(title="热榜",subtitle=f"{file[:5]} {file[6:8]}:{file[9:11]}"),
                yaxis_opts=opts.AxisOpts(name="热榜条目"),
                xaxis_opts=opts.AxisOpts(name="热度"),
            )
            .set_series_opts(label_opts=opts.LabelOpts(position="right"))
        )
        pie = (
            Pie()
            .add(
                series_name="舆情分布",
                data_pair=list(zip(["积极","中性","消极"], list(sentidata[cnt].values())[0])),
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
        cnt += 1
        grid = (
        Grid()
            .add(rank, grid_opts=opts.GridOpts(pos_right="20%"))
            .add(pie, grid_opts=opts.GridOpts(pos_left="20%"))
        )
        tl.add(grid,f"{file[:5]} {file[6:8]}:{file[9:11]}")
page.add(tl)

page.render('./out/Summary.html')
