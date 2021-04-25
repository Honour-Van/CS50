# -*-coding:utf-8-*-
import requests
from bs4 import BeautifulSoup
from datetime import datetime
# 根据地址获取页面内容，并返回BeautifulSoup


def format_time(cur_time: datetime, is_delta=True):
    return str(cur_time)[:19] if is_delta else str(cur_time)[:7]


def get_html(url):
    # 若页面打开失败，则无限重试，没有后退可言
    while True:
        try:
            # 超时时间为1秒
            response = requests.get(url, timeout=1)
            response.encoding = "GBK"  # 必须要用这个？
            if response.status_code == 200:
                return BeautifulSoup(response.text, "html.parser")
            else:
                continue
        except Exception:
            continue


# 获取地址前缀，从而构成下一级地址
def get_prefix(url):
    return url[0:url.rindex("/") + 1]


tab = ""

# 递归抓取下一页面


def spider_next(url, lev):
    if lev == 2:
        spider_class = "city"
    elif lev == 3:
        spider_class = "county"
    elif lev == 4:
        spider_class = "town"
    else:
        spider_class = "village"
    global tab
    tab += "\t"
    has_cur_lev = 0
    for item in get_html(url).select("tr." + spider_class + "tr"):
        item_td = item.select("td")
        item_td_code = item_td[0].select_one("a")
        item_td_name = item_td[1].select_one("a")
        if item_td_code is None:
            item_href = None
            item_code = item_td[0].get_text()
            item_name = item_td[1].get_text()
            if lev == 5:
                item_name = item_td[2].get_text() + item_td[1].get_text()
        else:
            item_href = item_td_code.get("href")
            item_code = item_td_code.get_text()
            item_name = item_td_name.get_text()
        content2 = tab
        content2 += item_code + item_name
        has_cur_lev = 1
        print(content2, file=wFile)

        tcs = datetime.now()
        if lev == 2 or lev == 3:
            print("["+format_time(tcs)+"] " + '*' *
                  (lev-1) + item_name + "开始爬取...", file=logFile)

        if item_href is not None:
            spider_next(get_prefix(url) + item_href, lev + 1)

        tce = datetime.now()
        if lev == 2 or lev == 3:
            print("["+format_time(tce)+"] " + '*' * (lev-1) +
                  item_name + "爬取完成，用时" + format_time((tce-tcs), False), file=logFile)

    tab = tab[:-1]
    if has_cur_lev is not True and lev != 5:
        spider_next(url, lev + 1)


# 入口
if __name__ == '__main__':
    # 抓取省份页面
    province_url = "http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2020/index.html"
    province_list = get_html(province_url).select('tr.provincetr a')
    wFile = open("StatData.txt", "w", encoding="utf-8")
    logFile = open("log.txt", 'w', encoding='utf-8')
    start_time = datetime.now()
    str(start_time)[:19]
    try:
        for province in province_list:
            href = province.get("href")
            province_code = href[0:2].ljust(12, '0')
            province_name = province.get_text()
            content = province_code + province_name
            print(content, file=wFile)

            tps = datetime.now()
            print("["+format_time(tps)+"] "+province_name+"开始爬取...", file=logFile)

            spider_next(get_prefix(province_url) + href, 2)

            tpe = datetime.now()
            print("["+format_time(tps)+"] "+province_name +
                  "爬取完成，用时" + format_time((tpe-tps), False), file=logFile)

        print("总用时：" + format_time((datetime.now()-start_time), False), file=logFile)
    finally:
        wFile.close()
        logFile.close()