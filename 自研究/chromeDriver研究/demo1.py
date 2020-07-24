from selenium import webdriver
from selenium.webdriver.chrome.options import Options





# 创建浏览器设置对象,用于保存你将要启动的浏览器的配置
chrome_opt = Options()

# 设置为无界面浏览器
# chrome_opt.add_argument('--headless')
# 设置窗口大小
chrome_opt.add_argument('--window-size=1366,768')
# 禁止图片加载
# prefs = {'profile.default_content_setting_values':{'images':2}}
# chrome_opt.add_experimental_option('prefs',prefs)









# 创建浏览器对象,这一行代码会打开浏览器
b = webdriver.Chrome(options=chrome_opt)
# 打开浏览器后,打开百度
b.get('http://www.geetest.com/Sensebot')
# 打印标题
print(b.title)

# # 添加cookie
# b.add_cookie({'name':"foo","value":"bar"})
# b.add_cookie({'name':"foo111","value":"bar111"})
#
# # 保存当前屏幕图片
# b.get_screenshot_as_file('demo.png')

# 获取窗口当前位置
# b.get_window_position()
# 获取浏览器窗口当前宽高以及位置
# b.get_window_rect()

# 获取元素的截图
# b.find_element_by_xpath('/html/body/div[3]/div[2]/div[1]/div/div[1]/div[1]/div/a/div[1]/div/canvas[1]')\
#     .screenshot('demo2.png')