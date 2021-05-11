import json
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

options = Options()
# options.add_argument("--headless")
browser = webdriver.Chrome(options=options)


browser.get("https://www.zhihu.com")
browser.maximize_window()


browser.delete_all_cookies()
cookie_filename = "./data/my_cookies.json"
cookies_file = open(cookie_filename, 'r', encoding='utf-8')
cookies = json.load(cookies_file)
for cookie in cookies:
    browser.add_cookie({
        'domain': '.zhihu.com',
        'name': cookie['name'],
        'value': cookie['value'],
        'path': '/',
        'expires': None
    })

browser.get("https://www.zhihu.com")
time.sleep(3)

browser.save_screenshot("./output/zhihu_login.png")

hot_button = browser.find_element_by_xpath("//a[@href='/hot']")
hot_button.click()


wait = WebDriverWait(browser, 10)
for i in range(100):  # 慢慢向下滑动窗口，让所有商品信息加载完成
    browser.execute_script('window.scrollTo(0, {});'.format(i*100))
    time.sleep(0.1)

wait.until(EC.presence_of_element_located(
    (By.XPATH, '//div[@class="HotList-end"]')), message="wait hotlist loading")  # 等待页面底部的当前页码出现
browser.save_screenshot("./output/zhihu_hot.png")

f = open("./output/hot.txt", 'w', encoding='utf-8')
print("知乎热榜：", datetime.now().strftime("%Y-%m-%d %H:%M:%S"), file=f)

soup = BeautifulSoup(browser.page_source, 'html.parser')
for item in soup.select("section.HotItem"):
    item_index = item.select("div.HotItem-rank")
    print(item_index[0].get_text(), file=f)
    item_title = item.select("h2.HotItem-title")
    print("问题：", item_title[0].get_text(), file=f)
    item_excerpt = item.select("p.HotItem-excerpt")
    if len(item_excerpt):
        print("概述：",item_excerpt[0].get_text(), file=f)
    item_metrics = item.select("div.HotItem-metrics")
    print("热度：",item_metrics[0].get_text()[:-7] + "万", file=f)