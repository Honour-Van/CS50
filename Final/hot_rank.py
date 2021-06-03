from bs4 import BeautifulSoup
from datetime import datetime
import json
import time
from selenium import webdriver

options = webdriver.chrome.options.Options()
options.add_argument("--headless")
browser = webdriver.Chrome(options=options)
wait = webdriver.support.wait.WebDriverWait(browser, 10)
browser.get("https://s.weibo.com/top/summary")
browser.maximize_window()

browser.delete_all_cookies()
cookie_filenam = "./data/weibo_cookies.json"
cookies_file = open(cookie_filenam, 'r', encoding='utf-8')
cookies = json.load(cookies_file)
for cookie in cookies:
    browser.add_cookie({
        'domain': cookie['domain'],
        'name': cookie['name'],
        'value': cookie['value'],
        'path': '/',
        'expires': None
    })

while True:
    try:
        time_stamp = datetime.now().strftime('%m-%d_%H-%M')
        f = open('./out/hotrank/' + time_stamp + ".txt", 'w', encoding='utf-8')
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
        time.sleep(60)
    except KeyboardInterrupt:
        break
    except:
        print(time_stamp, "failed")
        continue