from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import ActionChains
import random,time

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
b.get('https://passport.ceair.com/')
# 打印标题
print(b.title)

# source = b.find_element_by_xpath('/html/body/div/div[2]/div[6]/div/div[1]/div[2]/div[2]')
# actions = ActionChains(b)      # 创建动作链对象.
# actions.drag_and_drop_by_offset(source,100,0)
# actions.perform()

def get_tracks(distance):
    track=[]
    current=0
    mid=distance*3/4
    t=random.randint(2,3)/10
    v=0
    while current<distance:
          if current<mid:
             a=2
          else:
             a=-3
          v0=v
          v=v0+a*t
          move=v0*t+1/2*a*t*t
          current+=move
          track.append(round(move))
    return track

def move(location):

    # ActionChains(b).click_and_hold(element).perform()
    # tracks = get_tracks(location)
    # for track in tracks:
    #     print(f"移动了{track}")
    #     ActionChains(b).move_by_offset(track, 0).perform()
    #     time.sleep(0.01)
    #     # random.uniform(0.01, 0.07)
    # ActionChains(b).release(element).perform()

    slideblock = b.find_element_by_xpath('/html/body/div/div[2]/div[6]/div/div[1]/div[2]/div[2]')

    track_list = get_tracks(location + 3)
    # time.sleep(2)
    ActionChains(b).click_and_hold(slideblock).perform()
    # time.sleep(0.2)
    # 根据轨迹拖拽圆球
    for track in track_list:
        ActionChains(b).move_by_offset(xoffset=track, yoffset=0).perform()
    # 模拟人工滑动超过缺口位置返回至缺口的情况，数据来源于人工滑动轨迹，同时还加入了随机数，都是为了更贴近人工滑动轨迹
    # imitate = ActionChains(b).move_by_offset(xoffset=-1, yoffset=0)
    # time.sleep(0.015)
    # imitate.perform()
    # time.sleep(random.randint(6, 10) / 10)
    # imitate.perform()
    # time.sleep(0.04)
    # imitate.perform()
    # time.sleep(0.012)
    # imitate.perform()
    # time.sleep(0.019)
    # imitate.perform()
    # time.sleep(0.033)
    # ActionChains(b).move_by_offset(xoffset=1, yoffset=0).perform()
    # 放开圆球
    ActionChains(b).pause(random.randint(6, 14) / 10).release(slideblock).perform()
    time.sleep(2)


