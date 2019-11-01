import time
import psutil
import os
import socket
import requests
import zipfile
import threading
import shutil
import sendMessage
import threading
import subprocess
import time

class update_file():
    '''文件更新类'''
    def __init__(self):

        #=================================================
        self.server_root_url = "http://106.15.53.80:56789/" #服务器根目录
        #=================================================
        self.new_version_number = "" #最新版本号(v94)
        self.local_version_number = "" #本地版本号(v70)
        #=================================================
        self.server_new_version_url = "http://106.15.53.80:56789/newVersion.txt" #最新版本号获取地址
        self.local_new_version_url = "d:/DirectSpider/Version.txt" #本地版本号获取地址
        #=================================================
        self.new_file_name = "" #新版本文件名
        #=================================================
        self.file_download_state = False




    #=====================================================
    def get_new_version_number(self):
        '''获取服务器最新版本号'''

        try:
            url = self.server_new_version_url
            r = requests.get(url)
            self.new_version_number = (r.text).lower()
        except:
            print("获取服务器新版本号时失败")
    #===================================================== 
    def get_local_version_number(self):
        '''获取本地版本号'''
        try:
            has_file = os.path.exists(self.local_new_version_url) #判断有无此文件
            if has_file: #有
                with open(self.local_new_version_url,"r")as f:
                    self.local_version_number = f.read()
            else: #没有
                with open(self.local_new_version_url,"w",encoding="utf8")as f:
                    f.write("v1")
        except:
            print('获取本地版本号异常')
    #===================================================== 
    def get_file(self):
        '''下载最新文件并保存'''

        try:
            f = requests.get(self.server_root_url+self.new_version_number+".zip")
            with open(self.new_version_number+".zip","wb")as n_f:
                n_f.write(f.content)
                self.file_download_state = True
        except:
            print("下载文件错误")
        

    #===================================================== 

    def main(self):
        #获取服务器最新版本号
        self.get_new_version_number()
        print("最新版本号:",self.new_version_number)
        #获取当前版本号
        self.get_local_version_number()
        print("当前版本号:",self.local_version_number)
        #判断一致性
        same = self.local_version_number == self.new_version_number
        if same :
            print("已是最新版本,不更新")
            return
        else:
            print("线上有最新版,更新")
            self.get_file()
            if self.file_download_state:#下载文件成功
                print("下载文件成功")
                #解压文件


            else:
                print("下载文件失败")
                return

os.system("cls")
b = update_file()
b.main()