from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time




# 创建浏览器设置对象,用于保存你将要启动的浏览器的配置
chrome_opt = Options()
chrome_opt.add_argument('--window-size=1366,768')
# chrome_opt.add_experimental_option('excludeSwitches',['enable-automation'])

# 创建浏览器对象,这一行代码会打开浏览器
b = webdriver.Chrome(options=chrome_opt)
b.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
  "source": """
    Object.defineProperty(navigator, 'webdriver', {
      get: () => undefined
    })
  """
})
b.get('http://www.geetest.com/Sensebot')


print(b.title)
# 获取元素的截图
# b.find_element_by_xpath('/html/body/div[3]/div[2]/div[1]/div/div[1]/div[1]/div/a/div[1]/div/canvas[1]')\
#     .screenshot('demo2.png')

# 点击出现滑块
b.find_element_by_xpath('//*[@id="captcha"]/div[3]/div[2]/div[1]/div[3]').click()
#
# # 等待2秒
# time.sleep(2)
#
# b.find_element_by_xpath('/html/body/div[3]/div[2]/div[1]/div/div[1]/div[1]/div/a/div[1]/div/canvas[1]')\
#     .screenshot('code.png')
