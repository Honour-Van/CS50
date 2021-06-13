import json
from pyecharts.charts import Bar
from pyecharts.globals import ThemeType
import pyecharts.options as opts

with open('./data/date.json', 'r', encoding='utf-8') as f:
    date_list = json.load(f)

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

(
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
    .render('./out/wuhan_day_stack.html')
)