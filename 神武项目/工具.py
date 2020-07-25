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
TITLE = "神武4手游 - 浪淘沙"

# 图片识别接口认证码
APP_ID = '19321800'
API_KEY = 'wk15MCS4Vzn7mL5CFcegLhrl'
SECRET_KEY = 'p7fRKr1MAZimZbq3NTgZCF6R90ym7a52'

def 获取位置():
    句柄 = win32gui.FindWindow(None, TITLE)
    left, top, right, down = win32gui.GetWindowRect(句柄)

    with open("坐标表.json","r",encoding="UTF8")as f:
        pos_list = json.loads(f.read())

    for i in pos_list:
        if len(pos_list[i])==2:
            pos_list[i] = (left + pos_list[i][0], top + pos_list[i][1])
        else:
            pos_list[i] = (left + pos_list[i][0], top + pos_list[i][1],left+pos_list[i][2],top+pos_list[i][3])

    pos_list["窗口"] = (left,top,right,down)
    return pos_list

def 点击(坐标):

    # 鼠标移动到目标
    win32api.SetCursorPos(坐标)

    # 延迟0.5
    time.sleep(0.5)


    # 点击
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP | win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)

def 识别区域文字(区域坐标):

    # 根据传入位置截图并保存
    ImageGrab.grab(区域坐标).save(f"{区域坐标}.png")


    # 创建图片识别客户端
    client = AipOcr(APP_ID, API_KEY, SECRET_KEY)

    # 读取图片
    with open(f"{区域坐标}.png", 'rb') as fp:
        img = fp.read()

    # 读完删除
    os.remove(f"{区域坐标}.png")

    # 开始图片识别

    while True:
        res = client.basicGeneral(img);
        if "limit" in str(res):continue
        else:
            return str(res)

def 需求识别():
    句柄 = win32gui.FindWindow(None, TITLE)
    left, top, right, down = win32gui.GetWindowRect(句柄)
    im = ImageGrab.grab((left,top,right,down))

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

def 截图(位置):
    im = ImageGrab.grab(位置)
    im.save(f"{位置}.png")
    im.show()
if __name__ == '__main__':
    # 获取位置()
    位置 = 获取位置()
    print(截图(位置["窗口"]))