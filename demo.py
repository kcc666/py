# -*- coding: utf-8 -*-

import time
from selenium import webdriver
from lxml import html
from selenium.webdriver.chrome.options import Options

delay = 1

dep = "PUS"
arr = "MNL"
date = "2020-01-13"
nums = "PR419"

chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')

print("------------------------------------")
print("正在启动程序...")
b = webdriver.Chrome("d://chromedriver/chromedriver.exe",options=chrome_options)
b.get("https://flights.ctrip.com/international/search/oneway-{}-{}?depdate={}&cabin=y_s&adult=1&child=0&infant=0&directflight=".format(dep,arr,date))


print("正在加载航班信息...")
for i in range(8):
    b.execute_script("document.documentElement.scrollTop=10000")
    time.sleep(0.8)

print("正在解析航班信息...")
time.sleep(3)
t  = b.find_elements_by_xpath('//div[contains(@id,"{}")]/../../../div[@class="flight-seats"]'.format(nums))[0].text.replace("\n","")
print(t)
b.close()