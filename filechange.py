import time
import psutil
import os
import socket
import requests
import zipfile
import threading

new_version_path = 'http://106.15.53.80:56789/newVersion.txt'
current_version_path = "e://DirectSpider/Version.txt"
def get_new_version():
    '''获取最新版版本号'''
    try:
        r = requests.get(new_version_path)
        print(r.text)
        return r.text 
    except:
        print("获取最新版本号失败")
        return "f"

def get_current_version():
    '''获取本地路径最新版本号'''

    try:
        hasfile = os.path.exists(current_version_path)
        if hasfile:
            with open(current_version_path,"r",encoding="utf-8")as f:
                return f.read()
        else:
            with open(current_version_path,"w",encoding="utf-8")as f:
                f.write("新创建该文件")
    except:
        print("获取本地版本号失败")
        return "f"




def filechange():
    #获取版本号
    get_new_version()
    #获取当前版本号
    get_current_version()
    #比对两个版本号是否一致
    #版本号一致,不做修改

    #版本号不一致
        #下载最新版本号
        #解压到D盘目录
        #关闭DS程序,等待5秒
        #将解压得到的文件夹里的文件覆盖到DS目录
        #开启DS程序,
        #将D下的文件夹删掉
        #写入更新记录
    pass

if __name__ == "__main__":
    #文件更新
    filechange()
    #发送当前数据
    pass