import argparse
from bs4 import BeautifulSoup
import random
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
import json
import time
from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.webdriver.chrome.options import Options

with open('./data/hour.json', 'r', encoding='utf-8') as f:
    date_list = json.load(f)

s = len(date_list)-1  # 先排除掉最后一小时

parser = argparse.ArgumentParser(description='manual to this script')
parser.add_argument('-s', '--start-date', type=int, default=0)
parser.add_argument('-e', '--end-date', type=int, default=s)
args = parser.parse_args()
start_date = args.start_date
end_date = args.end_date

options = Options()
# options.add_argument("--headless")
browser = webdriver.Chrome(options=options)
wait = WebDriverWait(browser, 10)
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


def user_input(box, word):
    for char in word:
        box.send_keys(char)
        time.sleep(0.1 + random.uniform(-0.06, 0.06))
    box.send_keys(Keys.ENTER)


def change_time(index):
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

    item = date_list[index]
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

    item = date_list[index+1]
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


while True:
    try:
        browser.get("https://d.weibo.com/")
        input_box = browser.find_element_by_class_name("W_input")
        user_input(input_box, "武汉")

        fail_list = []
        try:
            for i in range(start_date, end_date):
                try:
                    change_time(i)
                    print(i, 'finished')
                except:
                    fail_list.append(i)
                    print(i, 'failed')
                soup = BeautifulSoup(browser.page_source, 'html.parser')
                y = date_list[i]['year']
                m = date_list[i]['month']
                d = date_list[i]['day']
                h = date_list[i]['hour']
                with open(f'./out/tmp/{y}-{str(int(m)+1)}-{str(d+1)}-{h}.txt', 'w', encoding='utf-8') as f:
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
