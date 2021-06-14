#!/usr/bin/env python
'''
@file:spider.py
@author: Honour-Van: fhn037@126.com
@description:爬虫对象类，框架文件
@version:1.0
'''


import argparse
from bs4 import BeautifulSoup
import random
from selenium.webdriver.common.keys import Keys
import json
import time
from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.webdriver.chrome.options import Options

class WeiboSpi():
    """
    @Description:微博爬虫类
    ---------
    @Param:无参数
    -------
    @Returns:返回一个用于爬取指定时间的类
    -------
    """
    def __init__(self):
        self.date_list = []
        self.hour_list = []

    def get_cookie(website="https://www.weibo.com", sitename='weibo'):
        options = Options()
        browser = webdriver.Chrome(options=options)
        browser.get(website)
        browser.maximize_window()

        input("请先登录，然后按回车……")

        cookies_dict = browser.get_cookies()
        cookies_json = json.dumps(cookies_dict)
        #print(cookies_json)

        # 登录完成后,将cookies保存到本地文件
        out_filename = f'./data/{sitename}_cookies.json'
        out_file = open(out_filename, 'w', encoding='utf-8')
        out_file.write(cookies_json)
        out_file.close()
        print('Cookies文件已写入：' + out_filename)

        browser.close()

    def generate_date(self, starttime=[], endtime=[], datefile = "./data/date.json", hourfile = "./data/hour.json"):
        # 生成目标时间节点
        if len(starttime) != 2 or len(endtime) != 2:
            raise Exception("time illegal, please don't use default param")
        
        y = starttime[0]
        if starttime[0] == endtime[0]:
            me = endtime[1]
        else:
            me = 12
        feb_day = 29 if y % 4 == 0 and y % 100 or y % 400 == 0 else 28
        for m in range(starttime[1]-1, me):
            monthday = 31
            if m == 2-1:
                monthday = feb_day
            elif m == 4-1 or m == 6-1 or m == 9-1 or m == 11-1:
                monthday = 30
            for d in range(monthday):
                self.date_list.append({'year':str(y), 'month':str(m), 'day':d})
                for h in range(24):
                    self.hour_list.append({'year':str(y), 'month':str(m), 'day':d, 'hour':str(h)})
        if starttime[0] == endtime[0]:
            return
        
        for y in range(starttime[0]+1, endtime[0]):
            feb_day = 29 if y % 4 == 0 and y % 100 or y % 400 == 0 else 28
            for m in range(12):
                monthday = 31
                if m == 2-1:
                    monthday = feb_day
                elif m == 4-1 or m == 6-1 or m == 9-1 or m == 11-1:
                    monthday = 30
                for d in range(monthday):
                    self.date_list.append({'year':str(y), 'month':str(m), 'day':d})
                    for h in range(24):
                        self.hour_list.append({'year':str(y), 'month':str(m), 'day':d, 'hour':str(h)})
        
        y = endtime[0]
        feb_day = 29 if y % 4 == 0 and y % 100 or y % 400 == 0 else 28
        for m in range(endtime[1]):
            monthday = 31
            if m == 2-1:
                monthday = feb_day
            elif m == 4-1 or m == 6-1 or m == 9-1 or m == 11-1:
                monthday = 30
            for d in range(monthday):
                self.date_list.append({'year':str(y), 'month':str(m), 'day':d})
                for h in range(24):
                    self.hour_list.append({'year':str(y), 'month':str(m), 'day':d, 'hour':str(h)})
        
        with open(hourfile, 'w', encoding='utf-8') as hour_file:
            json.dump(self.hour_list, hour_file)
        with open(datefile, 'w', encoding='utf-8') as date_file:
            json.dump(self.date_list, date_file)
    def get_date(self) -> list:
        # 获取已经生成的目标时间节点
        with open('./data/date.json', 'r', encoding='utf-8') as f:
            self.date_list = json.load(f)
        with open('./data/hour.json', 'r', encoding='utf-8') as f:
            self.hour_list = json.load(f)
        return len(self.hour_list)

    def start(self, output_dir="./out/wuhan_raw"):
        # 开始爬取
        def user_input(box, word):
            for char in word:
                box.send_keys(char)
                time.sleep(0.1 + random.uniform(-0.06, 0.06))
            box.send_keys(Keys.ENTER)
        def change_time(browser, index):
            """
            @Description:
            used to change start-time and end-time 
            ---------
            @Param:
            `index`: a integer points to one json dict in `date.json`
            -------
            @Returns
            None
            -------
            """
            advs = browser.find_element_by_css_selector("a[node-type='advsearch']")
            advs.click()

            item = self.date_list[index]
            y = item['year']
            m = item['month']
            d = item['day']
            hour = item['hour']

            stime = browser.find_element_by_css_selector("input[node-type='stime']")
            stime.click()
            s_month = Select(browser.find_element_by_class_name('month'))
            s_month.select_by_value(m)
            s_year = Select(browser.find_element_by_class_name('year'))
            s_year.select_by_value(y)
            day = browser.find_elements_by_css_selector("a[action-type='date']")
            day[d].click()
            s_hour = Select(browser.find_element_by_name('startHour'))
            s_hour.select_by_value(hour)
            time.sleep(0.1 + random.uniform(-0.06, 0.06))

            item = self.date_list[index+1]
            y = item['year']
            m = item['month']
            d = item['day']
            hour = item['hour']

            etime = browser.find_element_by_css_selector("input[node-type='etime']")
            etime.click()
            e_month = Select(browser.find_element_by_class_name('month'))
            e_month.select_by_value(m)
            e_year = Select(browser.find_element_by_class_name('year'))
            e_year.select_by_value(y)
            day = browser.find_elements_by_css_selector("a[action-type='date']")
            day[d].click()
            e_hour = Select(browser.find_element_by_name('endHour'))
            e_hour.select_by_value(hour)

            search_btn = browser.find_element_by_class_name('s-btn-a')
            search_btn.click()

        options = Options()
        # options.add_argument("--headless")
        browser = webdriver.Chrome(options=options)
        browser.get("https://d.weibo.com/")
        browser.maximize_window()
        # 导入cookie
        browser.delete_all_cookies()
        cookie_filename = "./data/weibo_cookies.json"
        cookies_file = open(cookie_filename, 'r', encoding='utf-8')
        cookies = json.load(cookies_file)
        for cookie in cookies:
            browser.add_cookie({
                'domain': cookie['domain'],
                'name': cookie['name'],
                'value': cookie['value'],
                'path': '/',
                'expires': None
            })

        s = self.get_date() - 1  # 先排除掉最后一小时
        parser = argparse.ArgumentParser(description='manual to this script')
        parser.add_argument('-s', '--start-date', type=int, default=0)
        parser.add_argument('-e', '--end-date', type=int, default=s)
        args = parser.parse_args()
        start_date = args.start_date
        end_date = args.end_date

        while True:
            try:
                browser.get("https://d.weibo.com/")
                input_box = browser.find_element_by_class_name("W_input")
                user_input(input_box, "武汉")

                fail_list = []
                try:
                    for i in range(start_date, end_date):
                        try:
                            change_time(browser, i)
                            print(i, 'finished')
                        except:
                            fail_list.append(i)
                            print(i, 'failed')
                        soup = BeautifulSoup(browser.page_source, 'html.parser')
                        y = self.date_list[i]['year']
                        m = self.date_list[i]['month']
                        d = self.date_list[i]['day']
                        h = self.date_list[i]['hour']
                        with open(f'{output_dir}/{y}-{str(int(m)+1)}-{str(d+1)}-{h}.txt', 'w', encoding='utf-8') as f:
                            for item in soup.select('p.txt'):
                                print(item.get_text(), file=f)
                except:
                    print(fail_list)
                    if len(fail_list) > 10:
                        raise
            except KeyboardInterrupt:
                print("next_time:", fail_list[0])
                break
            except:
                print("safer awful")
                start_date = fail_list[0]
                end_date = fail_list[-1]
                continue

if __name__ == "__main__":
    spider = WeiboSpi()
    # cookie和日期已经在实例中生成，因而可以直接跳过这两步，并直接登陆
    # spider.get_cookie()
    # spider.generate_date([2019,12], [2020,12])
    # spider.start('./out/wuhan_raw.txt')
    spider.start("./tmp") # 可以在tmp文件夹下进行简单的交互
