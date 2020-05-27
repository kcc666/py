#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: kcc time:2020/5/26

import win32gui
import win32con
import win32api
from PIL import ImageGrab
import time
from aip import AipOcr






title = "神武4手游 - 浪淘沙"

def 获取位置():
    # 获取窗口句柄
    句柄 = win32gui.FindWindow(None,title)
    left, top, right, down = win32gui.GetWindowRect(句柄)

    位置 = {
        "窗口":(left,top,right,down),
        "头像":[left + 880,top + 60],
        "宠物头像":[left + 720,top + 60],
        "世界地图":[left + 57,top + 80],
        "长安城":[left + 570,top + 550],
        "交易中心":[left + 425,top + 494],
        "小地图":[left + 130,top + 65],
        "修行":[left + 223,top + 70],
        "我要铜币":[left + 176,top + 343],
        "出售宠物":[left + 840,top + 435],
        "宠物名字区域":(left+580, top+160 ,left+670, top+190),
        "前往野外":[left + 740,top + 250],
        "寒冰宫一层":[left + 400,top + 330],
        "右下角区域":(left+960,top+715,left+1018,top+767),
        "捕捉区域":(left+729,top+752,left+780,top+788),
        "出售宠物按钮":[left + 894,top + 220],
    }

    return 位置

    #
def 点击(目标):
    # 鼠标定位到(30,50)
    win32api.SetCursorPos(目标)
    # 执行左单键击，若需要双击则延时几毫秒再点击一次即可
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP | win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)

def 截图(位置,文件名):
    # 截图
    ImageGrab.grab(位置).save(f"{文件名}.png")
    print("截图已保存")

def 到宠物交易中心():
    位置 = 获取位置()
    点击(位置["修行"])
    time.sleep(1)
    点击(位置["我要铜币"])
    time.sleep(1)
    点击(位置["出售宠物"])
    time.sleep(0.5)
    点击(位置["出售宠物"])
    time.sleep(10)
    print("已到达宠物中心")

def 前往野外():
    位置 = 获取位置()
    点击(位置["前往野外"])
    time.sleep(1)
    点击(位置["寒冰宫一层"])
    time.sleep(0.5)
    点击(位置["寒冰宫一层"])

def 判断战斗状态():
    位置 = 获取位置()
    截图(位置["右下角区域"],"右下角区域")

def 图片识别(filePath):
    APP_ID = '19321800'
    API_KEY = 'wk15MCS4Vzn7mL5CFcegLhrl'
    SECRET_KEY = 'p7fRKr1MAZimZbq3NTgZCF6R90ym7a52'

    client = AipOcr(APP_ID, API_KEY, SECRET_KEY)

    with open(filePath, 'rb') as fp:
        image = fp.read()

    res = client.basicGeneral(image);
    print(res)


if __name__ == '__main__':
    位置 = 获取位置()
    # 到宠物交易中心()
    # 前往野外()
    # 判断战斗状态()
    # 截图(位置["宠物名字区域"],"宠物区域")
    # 截图((0,0,3810,1080),"全屏")
    # 任意位置到宠物交易中心
    截图(位置["捕捉区域"],"捕捉区域")

    图片识别("捕捉区域.png")



    # 出售宠物
    # 捕捉宠物
    # 第一回合打击,第二回合之后捕捉,
    # 图片识别
        # 判断是否在战斗状态
        # 判断手里有几只宠物
        # 判断敌对有几只宠物

