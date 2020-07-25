import requests
import traceback
import os
import win32gui
import win32con
import win32api
from PIL import ImageGrab,Image
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
        "购买": (left + 648, top + 666),
        "n1":(left+547,top+229),
        "n2":(left+794,top+232),
        "n3":(left+541,top+331),
        "n4":(left+796,top+325),
        "n5":(left+526,top+411),
        "n6":(left+785,top+410),
        "n7":(left+545,top+494),
        "n8":(left+789,top+497),
        "n9":(left+537,top+582),
        "n10":(left+787,top+587),
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
    os.remove(f"{位置}.png")

    # 开始图片识别

    while True:
        res = client.basicGeneral(img);
        if "limit" in str(res):continue
        else:
            # # for i in res["words_result"]:
            # #     print(i["words"])
            # print(res)
            # break
            return str(res)

def 需求识别(位置):
    # im = Image.open(f"{位置}.png")
    im = ImageGrab.grab(位置)
    pix = im.load()
    pos = [
        {"基准点":(415,197),"需求":(445,197),"售罄":(414,222)},
        {"基准点":(658,197),"需求":(688,197),"售罄":(654,222)},
        {"基准点":(415,286),"需求":(445,286),"售罄":(414,311)},
        {"基准点":(658,286),"需求":(688,286),"售罄":(654,311)},
        {"基准点":(415,375),"需求":(445,375),"售罄":(414,400)},
        {"基准点":(658,375),"需求":(688,375),"售罄":(654,400)},
        {"基准点":(415,464),"需求":(445,464),"售罄":(414,489)},
        {"基准点":(658,464),"需求":(688,464),"售罄":(654,489)},
        {"基准点":(415,553),"需求":(445,553),"售罄":(414,578)},
        {"基准点":(658,553),"需求":(688,553),"售罄":(654,578)}
    ]

    result = {
        "n1":False,
        "n2":False,
        "n3":False,
        "n4":False,
        "n5":False,
        "n6":False,
        "n7":False,
        "n8":False,
        "n9":False,
        "n10":False,
    }

    像素差 = 10
    for i,v in enumerate(pos,start=1):
        需求像素值 = pix[v["需求"][0],v["需求"][1]]


        if abs(需求像素值[0]-245) in range(像素差):
            result[f"n{i}"] = True

    return result




if __name__ == '__main__':


    位置 = 获取位置()
    # r = 需求识别(位置["窗口"])
    # print(r)
    # 点击(位置["n2"])
    if "需求" in 识别区域(位置["古董"]):
        print("有需求")
        列表 = 需求识别(位置["窗口"])
        for i in 列表:
            if 列表[i]:
                点击(位置[i])
                time.sleep(0.5)
                点击(位置["购买"])
                break
    else:
        print("无需求")