import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options #用于设置浏览器启动的一些参数

def get_cookie(website, sitename):
    options = Options()
    #options.add_argument("--headless")  # 不打开浏览器界面，以节省时间
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

if __name__ == "__main__":
    get_cookie('https://www.weibo.com', 'weibo')
    