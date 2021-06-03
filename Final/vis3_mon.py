import json
from pyecharts.charts import Bar
from pyecharts import options as opts

with open('./out/wuhan_stat_mon.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
(
    Bar()
    .add_xaxis(list(data.keys()))
    .add_yaxis("positive count", [(item[1]['positive cnt']/(item[1]['positive cnt']+item[1]['neutral cnt']+item[1]['negative cnt'])) for item in data.items()], stack='stack1')
    .add_yaxis("neutral count", [(item[1]['neutral cnt']/(item[1]['positive cnt']+item[1]['neutral cnt']+item[1]['negative cnt'])) for item in data.items()], stack='stack1')
    .add_yaxis("negative count", [item[1]['negative cnt']/(item[1]['positive cnt']+item[1]['neutral cnt']+item[1]['negative cnt']) for item in data.items()], stack='stack1')
    .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
    .set_global_opts(title_opts=opts.TitleOpts(title="武汉微博舆情-按月"),datazoom_opts=opts.DataZoomOpts())
    .render('./out/wuhan_bymonth.html')
)