from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.wait import WebDriverWait
import time
driver = webdriver.Chrome()
# driver.implicitly_wait(10)

driver.get("http://ibook.himytrip.com/default.aspx")

WebDriverWait(driver,10,0.5).until(lambda el:driver.find_element_by_xpath('//skkk'))


# 隐式等待:调用find_element方法时,隐式等待时间内未返回,则等着,如有返回,则执行下一行代码,超出隐式等待时间就抛异常(针对全局所有元素)

# 显示等待:调用WebDriverWait方法时,指定时间内按照指定频率查某元素,没查到则继续查,查到了往下执行,超出指定时间就抛异常(针对单个元素)

# 要避免的坑:
# 元素定位: