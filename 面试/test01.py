import argparse
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By



# 实例化出一个chrome浏览器设置
chrome_options = Options()

# 基础设置
prefs = {
    # 禁止加载图片
    "profile.managed_default_content_settings.images": 2,
    # 禁用css
    'permissions.default.stylesheet': 2,
    # 禁止弹窗
    'profile.default_content_setting_values': {'notifications': 2}
}


# # chrome_options.add_experimental_option("prefs", prefs)
chrome_options.add_experimental_option('useAutomationExtension', False)


# 设置为开发者模式
chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
#
# # 浏览器异常忽略
chrome_options.add_argument('--ignore-certificate-errors')
chrome_options.add_argument('--ignore-ssl-errors')
chrome_options.add_argument('--ignore-certificate-errors-spki-list')
chrome_options.add_argument('--allow-insecure-localhost')
#
# # 懒加载模式，不等待页面加载完毕
capa = DesiredCapabilities.CHROME
capa["pageLoadStrategy"] = "none"

driver = webdriver.Chrome(
    options=chrome_options,
    # desired_capabilities=capa
    )

driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
  "source": """
    Object.defineProperty(navigator, 'webdriver', {
      get: () => undefined
    })
  """
})

driver.execute_cdp_cmd("Network.enable", {})
driver.execute_cdp_cmd("Network.setExtraHTTPHeaders", {"headers": {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.87 Safari/537.36"}})

driver.get("http://wenshu.court.gov.cn/")


# driver.find_element_by_xpath('//*[@id="_view_1540966814000"]/div/div[1]/div[2]/input').send_keys("深圳")
driver.find_element_by_xpath('//*[@id="_view_1540966814000"]/div/div[1]/div[3]').click()

# # 设置浏览器窗口的位置和大小
# driver.set_window_position(20, 40)
# driver.set_window_size(1200, 800)
