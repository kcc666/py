import requests
import traceback
import os
import win32gui
import win32con
import win32api
from PIL import ImageGrab
import time
from aip import AipOcr
import json
import random
# from json.decoder import JSONDecodeError


title = "神武4手游 - 浪淘沙"

def 问(q):

    try:
        r = requests.get(url=f"http://tapi.gfun.me/sw3/kj/api.php?text={q}").json()
        # print(r)
        if "查询为空" in str(r):
            print("无该答案")

        for i in r["data"]:
            print(f"问:{i[0]}|答:{i[1]}")
    except:
        return "请求异常"

def 获取位置():
    # 获取窗口句柄
    句柄 = win32gui.FindWindow(None,title)
    left, top, right, down = win32gui.GetWindowRect(句柄)

    位置 = {
        "窗口":(left,top,right,down),
        "日程":(left+380,top+80),
        "竞技场":(left+700,top+230),
        "战斗状态":(left+960,top+715,left+1020,top+775),
        "自动":(left+990,top+745),
        "挑战1":(left+890,top+210),
        "挑战2":(left+890,top+300),
        "挑战3":(left+890,top+390),
        "挑战4":(left+890,top+490),
        "挑战5":(left+890,top+585),
        "问题":(left+303,top+263,left+737,top+410),
    }

    return 位置

def 截图(位置,文件名):
    # 截图
    ImageGrab.grab(位置).save(f"{文件名}.png")
    # ImageGrab.grab(位置).show()

def 图片识别(imgname):
    APP_ID = '19321800'
    API_KEY = 'wk15MCS4Vzn7mL5CFcegLhrl'
    SECRET_KEY = 'p7fRKr1MAZimZbq3NTgZCF6R90ym7a52'

    client = AipOcr(APP_ID, API_KEY, SECRET_KEY)

    with open(imgname+".png", 'rb') as fp:
        img = fp.read()

    os.remove(imgname+".png")

    res = client.basicGeneral(img);

    if "words_result" not in str(res):return "未识别到文字"
    if not res["words_result"]:return "未识别到文字"


    for i in res["words_result"]:
        return i["words"].replace("“","").replace("”","")\
        .replace("《","").replace("》","")

if __name__ == '__main__':


    current = ""

    while 1:
        位置 = 获取位置()
        截图(位置["问题"],"问题")
        q = 图片识别("问题")
        if q==current:
            time.sleep(3)
            continue
        else:
            current = q
            print(q)

            if q == "未识别到文字":
                print("图片识别未识别到文字")
            else:
                print("正在查找答案")
                问(q[:5])

