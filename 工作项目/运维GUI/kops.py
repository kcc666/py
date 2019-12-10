#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: kcc time:2019/12/9

import tkinter
import threading
import requests
import time
import json


class CsharpUpdate():
    def __init__(self):

        self.new_version_url = 'http://106.15.53.80:56789/newversion.txt' # C#新版本号获取地址
        self.local_version_url = 'D://DirectSpider/version.txt' # C#本地版本号地址

        self.new_version = ""
        self.local_version = ""

    def main(self):
        #1 获取最新版本号
        self.new_version =  self.get_new_version()
        #2 获取本地版本号
        self.local_version = self.get_local_version()

        if self.new_version == self.local_version:
            print("版本一致,不更新")
        else:
            print("版本不一致,更新")

    def get_new_version(self):
        #获取最新版本号
        try:
            r = requests.get(self.new_version_url)
            if r.status_code == 200:
                return r.text
            else:
                self.log('err',r.status_code+"|get_new_version")

        except BaseException as e:
            self.log('err',str(e)+"|get_new_version")

    def get_local_version(self):
        #获取本地版本号
        if not self.new_version:return #限定前一个步骤未执行成功,本函数不执行

        try:
            with open("version.json","r")as f:
               return json.loads(f.read())["cversion"]

        except BaseException as e:
            self.log('err',str(e)+"|get_local_version")

    def down_file(self):
        #下载文件
        pass
    def unzip(self):
        #解压文件
        pass
    def open_close(self):
        #打开或关闭文件
        pass
    def copy_file(self):
        #拷贝和覆盖文件
        pass
    def log(self,type,text):
        timenow = time.strftime("%Y-%m-%d %X")
        if type == "err":
            with open('errlog.txt',"a",encoding="utf8")as f:
                f.write(str(text)+"|"+timenow)
        elif type == "update":
            with open('update.txt', "a", encoding="utf8")as f:
                f.write(str(text) + "|" + timenow)
        else:
            return




    def del_file(self):
        #删除多余的文件
        pass

CsharpUpdate().main()