from pyecharts.faker import Faker
from pyecharts import options as opts
from pyecharts.charts import Map
import json

gdp_dict = {}
agdp_dict = {}
with open('./assets/GDP.json', 'r', encoding='utf-8') as f:
    gdp_dict = json.load(f)
with open('./assets/GDP_ave.json', 'r', encoding='utf-8') as f:
    agdp_dict = json.load(f)

[[country[0], country[1]] for country in gdp_dict.items()]
(
    Map()
    .add("GDP/$1trillion", 
         [[country[0], country[1]] for country in gdp_dict.items()], 
         maptype="world",
         is_map_symbol_show=False,  # 不描点
    )
    .add("Average GDP/$10thousand", 
         [[country[0], country[1]] for country in agdp_dict.items()], 
         maptype="world",
         is_map_symbol_show=False,  # 不描点
         is_selected=False,
         max_scale_limit=12
    )
    .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
    .set_global_opts(
        title_opts=opts.TitleOpts(title="GDP Top10 in 2019"),
        visualmap_opts=opts.VisualMapOpts(max_=22, is_piecewise=True),
    )
    .render('./out/map_world_gdp.html')
)

import os 
os.system("start chrome ./out/map_world_gdp.html")