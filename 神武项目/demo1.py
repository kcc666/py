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
import 坐标表
import copy



def 识别区域文字(区域坐标):
    APP_ID = '19321800'
    API_KEY = 'wk15MCS4Vzn7mL5CFcegLhrl'
    SECRET_KEY = 'p7fRKr1MAZimZbq3NTgZCF6R90ym7a52'
    client = AipOcr(APP_ID, API_KEY, SECRET_KEY)


    with open(f"{区域坐标}.jpg", 'rb') as fp:
        img = fp.read()

    # 读完删除

    # 开始图片识别

    while True:
        res = client.basicGeneral(img);
        # print(res)
        if "limit" in str(res) or "words_result" not in str(res):continue
        else:
            r = ""
            for i in res["words_result"]:
                r += i["words"]+"\n"
            return r


if __name__ == '__main__':
    识别区域文字("C:\\User\\46321\\Desktop\\神武临时\\宝图完毕1")

    #r"C:\Users\46321\Desktop\神武临时\宝图完毕"
