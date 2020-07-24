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


# 窗口标题
title = "神武4手游 - 浪淘沙"

# 图片识别接口认证码
APP_ID = '19321800'
API_KEY = 'wk15MCS4Vzn7mL5CFcegLhrl'
SECRET_KEY = 'p7fRKr1MAZimZbq3NTgZCF6R90ym7a52'

def 点击(目标):
    # 鼠标移动到目标
    win32api.SetCursorPos(目标)
    # 延迟0.5
    time.sleep(0.5)

    # 点击
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP | win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)

    # time.sleep(0.1)
    # win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP | win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)

def 获取位置():
    # 获取窗口句柄
    句柄 = win32gui.FindWindow(None,title)
    left, top, right, down = win32gui.GetWindowRect(句柄)

    位置 = {
        "窗口":(left,top,right,down),
        "装备":(left+177,top+298,left+361,top+328),
        "烹饪":(left+174,top+340,left+366,top+374),
        "草药丹药":(left+177,top+386,left+367,top+417),
        "高品丹药":(left+178,top+431,left+366,top+461),
        "古董":(left+179,top+476,left+366,top+506),
        "n1":(left+416,top+198,left+485,top+265),
        "n2":(left+658,top+198,left+721,top+265),
        "n3":(left+413,top+287,left+482,top+351),
        "n4":(left+659,top+287,left+724,top+351),
        "n5":(left+416,top+377,left+482,top+441),
        "n6":(left+659,top+376,left+725,top+441),
        "n7":(left+416,top+466,left+483,top+531),
        "n8":(left+659,top+465,left+725,top+531),
        "n9":(left+414,top+552,left+447,top+591),
        "n10":(left+655,top+555,left+725,top+619),
    }

    return 位置

def 识别区域(位置):

    # 根据传入位置截图并保存
    ImageGrab.grab(位置).save(f"{位置}.png")

    # 创建图片识别客户端
    client = AipOcr(APP_ID, API_KEY, SECRET_KEY)

    # 读取图片
    with open(f"{位置}.png", 'rb') as fp:
        img = fp.read()

    # 读完删除
    # os.remove(f"{位置}.png")

    # 开始图片识别

    while True:
        res = client.basicGeneral(img);
        if "limit" in str(res):continue
        else:
            # for i in res["words_result"]:
            #     print(i["words"])
            print(res)
            break


if __name__ == '__main__':


    位置 = 获取位置()
    识别区域(位置["n1"])
    识别区域(位置["n2"])
    识别区域(位置["n3"])
    识别区域(位置["n4"])
    识别区域(位置["n5"])
    识别区域(位置["n6"])
    识别区域(位置["n7"])
    识别区域(位置["n8"])
    识别区域(位置["n9"])
    识别区域(位置["n10"])


