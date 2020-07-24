from selenium.webdriver import Chrome
from selenium.webdriver import ChromeOptions



b = Chrome()
b.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
  "source": """
    Object.defineProperty(navigator, 'webdriver', {
      get: () => undefined
    })
  """
})
b.get('http://www.geetest.com/Sensebot')
# b.get('http://www.kongcc.com')