#!/usr/bin/env python
'''
@file:hot_rank.py
@author: Honour-Van: fhn037@126.com
@description:部署在服务器端的爬虫
@version:1.0
'''


from bs4 import BeautifulSoup
from datetime import datetime
import json
import time
from selenium import webdriver

options = webdriver.chrome.options.Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")

browser = webdriver.Chrome(options=options)
wait = webdriver.support.wait.WebDriverWait(browser, 10)
browser.get("https://s.weibo.com/top/summary")
browser.maximize_window()

browser.delete_all_cookies()
cookies = json.loads('[{"domain": ".weibo.com", "expiry": 1620805311, "httpOnly": false, "name": "webim_unReadCount", "path": "/", "secure": false, "value": "%7B%22time%22%3A1620718911632%2C%22dm_pub_total%22%3A0%2C%22chat_group_client%22%3A0%2C%22chat_group_notice%22%3A0%2C%22allcountNum%22%3A0%2C%22msgbox%22%3A0%7D"}, {"domain": ".weibo.com", "expiry": 1652254908, "httpOnly": false, "name": "UOR", "path": "/", "secure": false, "value": ",,graph.qq.com"}, {"domain": ".weibo.com", "expiry": 1621323705, "httpOnly": false, "name": "wvr", "path": "/", "secure": false, "value": "6"}, {"domain": ".weibo.com", "expiry": 1652254905, "httpOnly": false, "name": "SUBP", "path": "/", "sameSite": "None", "secure": true, "value": "0033WrSXqPxfM725Ws9jqgMF55529P9D9W5MXGO8S9jl0rP4Vn2I2IK45NHD95QcSoBXeKBRS0ecWs4DqcjeCsvVdNHEHJ8VeKzc"}, {"domain": "weibo.com", "expiry": 1620748788, "httpOnly": false, "name": "wb_view_log_6644148736", "path": "/", "secure": false, "value": "1707*10671.5"}, {"domain": "weibo.com", "expiry": 1620748750, "httpOnly": false, "name": "wb_view_log", "path": "/", "secure": false, "value": "1707*10671.5"}, {"domain": ".weibo.com", "expiry": 1652254905, "httpOnly": true, "name": "SUB", "path": "/", "sameSite": "None", "secure": true, "value": "_2A25NnkVoDeThGeBI71YQ9CbLyDqIHXVvYWsgrDV8PUJbkNB-LUf7kW1NRpyGWBsY9JCfGvXAl8budWw-T5NaG-bf"}, {"domain": ".weibo.com", "httpOnly": false, "name": "SSOLoginState", "path": "/", "sameSite": "None", "secure": true, "value": "1620718904"}, {"domain": ".weibo.com", "httpOnly": false, "name": "Apache", "path": "/", "secure": false, "value": "3221964407714.939.1620718870167"}, {"domain": ".weibo.com", "httpOnly": false, "name": "_s_tentry", "path": "/", "secure": false, "value": "passport.weibo.com"}, {"domain": "weibo.com", "expiry": 1620719469, "httpOnly": false, "name": "WBStorage", "path": "/", "secure": false, "value": "202105111541|undefined"}, {"domain": ".weibo.com", "expiry": 1651822870, "httpOnly": false, "name": "ULV", "path": "/", "secure": false, "value": "1620718870170:1:1:1:3221964407714.939.1620718870167:"}, {"domain": ".weibo.com", "httpOnly": false, "name": "cross_origin_proto", "path": "/", "secure": false, "value": "SSL"}, {"domain": ".weibo.com", "expiry": 1620719476, "httpOnly": true, "name": "crossidccode", "path": "/", "secure": false, "value": "CODE-yf-1LGn11-26H7sP-i8nKi7WrMnrp5sS23cefa"}, {"domain": ".weibo.com", "expiry": 1936078870, "httpOnly": false, "name": "SINAGLOBAL", "path": "/", "secure": false, "value": "3221964407714.939.1620718870167"}, {"domain": ".weibo.com", "httpOnly": false, "name": "login_sid_t", "path": "/", "secure": false, "value": "857dabbe6b0caf7a49d0eebe46dd0d0f"}]')
for cookie in cookies:
    browser.add_cookie({
        'domain': cookie['domain'],
        'name': cookie['name'],
        'value': cookie['value'],
        'path': '/',
        'expires': None
    })

# 反复抓取
while True:
    try:
        time_stamp = datetime.now().strftime('%m-%d_%H-%M')
        f = open('./out/' + time_stamp + ".txt", 'w', encoding='utf-8')
        browser.get("https://s.weibo.com/top/summary")
        soup = BeautifulSoup(browser.page_source, 'html.parser')
        rows = soup.select("#pl_top_realtimehot table tbody tr")
        for row in rows:
            hc = row.find('a')
            if hc.get_text() != '':
                hot_cot = hc.get_text()
            hv_tmp = row.find('span')
            if hv_tmp and hv_tmp.get_text() != '':
                hot_val = hv_tmp.get_text()
                print(hot_cot+','+hot_val, file=f)
        f.close()
        print(time_stamp, 'yes!')
        time.sleep(60)
    except KeyboardInterrupt:
        break
    except:
        print(time_stamp, "failed")
        continue