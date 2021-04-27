#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@file:stat_spider.py
@author: Honour-Van: fhn037@126.com
@date:2021/04/21 22:26:04
@description: get data from the website with friendly Chinese UI
'''

import requests
from bs4 import BeautifulSoup
from datetime import datetime

def format_time(cur_time: datetime, is_delta=True):
    """
    # format_time
    @Description:
    transform the datetime.datetime into assigned long format
    ---------
    @Param:
    cur_time: a datetime object, with full precision
    is_delta: a timedelta object, with full precision with less length
    -------
    @Returns:
    a str that with the form like yyyy-mm-dd hh:mm:ss
                        or h:mm:ss if object is timedelta
    -------
    """
    return str(cur_time)[:19] if is_delta else str(cur_time)[:7]


def get_html(url):
    """
    # get_html
    @Description:
    get html code by url 
    based on exception handling and anti-spider design 
    to realize totally data mining
    ---------
    @Param:
    a url str
    -------
    @Returns:
    a Beautifulsoup object
    GBK encoding and html.parser as resolver.
    -------
    """
    while True:
        try:
            response = requests.get(url, timeout=1) # set appropriate timeout to reduce the possibilities of anti-
            response.encoding = "GBK"
            if response.status_code == 200: # if access successfully
                return BeautifulSoup(response.text, "html.parser")
            else:
                continue
        except Exception:
            continue


def get_prefix(url):
    """
    @Description:
    get the prefix of a url
    to form the sub-level url
    ---------
    @Param:
    url:str
    -------
    @Returns:
    a substr end where '/' last time appears
    -------
    """
    return url[0:url.rfind("/") + 1]


indent = ""

# 递归抓取下一页面


def spider_next(url, lev):
    """
    # spider_next
    @Description:
    core function of spider
    with recursive structure to traverse all the nodes in it 
    ---------
    @Param:
    url: str
    lev: recursive level
    -------
    @Returns:
    recursion, void type
    -------
    """
    # choose spider_class in order to select specific table elements in specific page
    if lev == 2:
        spider_class = "city"
    elif lev == 3:
        spider_class = "county"
    elif lev == 4:
        spider_class = "town"
    else:
        spider_class = "village"
    # indent is used to format the output 
    global indent
    indent += "\t"
    has_cur_lev = 0 # becaution to that dongguan has only four levels, we use this to gap the missing lev
    for item in get_html(url).select("tr." + spider_class + "tr"): # select the assigned table row data
        item_td = item.select("td")
        item_td_code = item_td[0].select_one("a")
        item_td_name = item_td[1].select_one("a")
        if item_td_code is None: # some td has no link with it
            item_href = None
            item_code = item_td[0].get_text() # it can get the text even it has an enter symbol following it 
            item_name = item_td[1].get_text()
            if lev == 5:
                item_name = item_td[2].get_text() + item_td[1].get_text() 
                # the most childist ones has different output format with a identification code
        else:
            item_href = item_td_code.get("href")
            item_code = item_td_code.get_text()
            item_name = item_td_name.get_text()
        content2 = indent
        content2 += item_code + item_name
        has_cur_lev = 1
        print(content2, file=wFile)

        tcs = datetime.now() #time count
        if lev == 2 or lev == 3:
            print("["+format_time(tcs)+"] " + '*' *
                  (lev-1) + item_name + "开始爬取...")

        if item_href is not None: # recursion
            spider_next(get_prefix(url) + item_href, lev + 1)

        tce = datetime.now()
        if lev == 2 or lev == 3:
            print("["+format_time(tce)+"] " + '*' * (lev-1) +
                  item_name + "爬取完成，用时" + format_time((tce-tcs), False))
        if lev == 2:
            print("--------------------------------------------------------")
    indent = indent[:-1]
    if has_cur_lev is not True and lev != 5: # deal with those ones without full 5 levels, directly deep in
        spider_next(url, lev + 1)


if __name__ == '__main__':
    province_url = "http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2020/index.html"
    province_list = get_html(province_url).select('tr.provincetr a') # get the province list
    wFile = open("StatData.txt", "w", encoding="utf-8")
    start_time = datetime.now()
    str(start_time)[:19]
    try:
        for province in province_list: # traverse the province list, 
            # in fact it can be inserted into the recursion structure
            href = province.get("href")
            province_code = href[0:2].ljust(12, '0')
            province_name = province.get_text()
            content = province_code + province_name
            print(content, file=wFile)

            tps = datetime.now()
            print("["+format_time(tps)+"] "+province_name+"开始爬取...")

            spider_next(get_prefix(province_url) + href, 2) # start a province's spider

            tpe = datetime.now()
            print("["+format_time(tps)+"] "+province_name +
                  "爬取完成，用时" + format_time((tpe-tps), False))
            print("========================================================")
            
        print("总用时：" + format_time((datetime.now()-start_time), False))
    finally:
        wFile.close()