from selenium import webdriver
import os
#设置为不弹出chrome
# options = webdriver.ChromeOptions()
# options.add_argument('--headless')

driver = webdriver.Chrome(r"D:\chromedriver\chromedriver.exe")

#打开chrome
driver.get("https://www.eastarjet.com/newstar/PGWHC00001")
# driver.get("http://www.baidu.com")

#获得cookie:       driver.get_cookies()
#设置窗口大小:      driver.set_window_size(1920,1080)
#input框输入内容:   send_keys("输入内容")

#点掉提示框
# driver.find_element_by_id("PNWHC000018_close").click()

#点选单程
# driver.find_elements_by_class_name("iCheck-helper")[1].click()

# 注入JS
with open ("spider.js","r",encoding="utf8")as f:
    js = f.read()
    driver.execute_script(js)


#页面截屏
# driver.save_screenshot("baidu.png")

#关闭chrome
# driver.quit()