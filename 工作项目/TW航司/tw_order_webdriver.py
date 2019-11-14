from selenium import webdriver
import os

print('*'*40)
# print(os.path.dirname(__file__))
os.chdir(os.path.dirname(__file__))
print('*'*40)

#设置webdriver不加载图片
chrome_opt = webdriver.ChromeOptions()
chrome_opt.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2})

#启动webdriver
browser = webdriver.Chrome()

#打开主页
browser.get("https://www.twayair.com/app/main")

#点击登录
browser.find_element_by_class_name("btn_login").click()

#输入账号
browser.find_element_by_id("loginId").send_keys("Aa960319")
#输入密码
browser.find_element_by_id("loginPassword").send_keys("himyidea123")
#点击登录
browser.find_elements_by_css_selector('.btn_large.red.wp100')[0].click()
