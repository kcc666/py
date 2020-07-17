#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: kcc time:2020/5/26

# import pywin32
import os
import win32gui
import win32con
import win32api
from PIL import ImageGrab
import time
from aip import AipOcr
import json
import random

title = "神武4手游 - 浪淘沙"


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
        "挑战5":(left+890,top+585)
    }

    return 位置



def 点击(目标):
    # 鼠标定位到(30,50)
    win32api.SetCursorPos(目标)
    time.sleep(0.5)
    # 执行左单键击，若需要双击则延时几毫秒再点击一次即可
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP | win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    time.sleep(0.1)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP | win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
def 截图(位置,文件名):
    # 截图
    ImageGrab.grab(位置).save(f"{文件名}.png")
    # ImageGrab.grab(位置).show()


def 判断战斗状态():
    cnt = 0
    while True:
        位置 = 获取位置()
        截图(位置["战斗状态"],"战斗状态")
        res = 图片识别("战斗状态")

        if "自" in res or "动" in res:
            print("战斗状态")
            time.sleep(10)
            cnt+=10
            print(f"本回合已持续{cnt}秒")
        else:
            print("非战斗状态,回合结束")
            break


def 图片识别(imgname):
    APP_ID = '19321800'
    API_KEY = 'wk15MCS4Vzn7mL5CFcegLhrl'
    SECRET_KEY = 'p7fRKr1MAZimZbq3NTgZCF6R90ym7a52'

    client = AipOcr(APP_ID, API_KEY, SECRET_KEY)

    with open(imgname+".png", 'rb') as fp:
        img = fp.read()

    os.remove(imgname+".png")

    res = client.basicGeneral(img);
    return str(res)

if __name__ == '__main__':
    位置 = 获取位置()

    点击(位置["日程"])
    time.sleep(2)

    点击(位置["竞技场"])
    time.sleep(2)

    while True:

        i = str(random.randint(1,5))
        点击(位置[f"挑战{i}"])
        time.sleep(2)

        点击(位置["自动"])
        time.sleep(2)

        判断战斗状态()

        time.sleep(5)


#
