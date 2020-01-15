import time
import psutil
import os
import socket
import requests
import zipfile
import threading
import shutil
import threading
import subprocess
import json
import multiprocessing
# os.system('taskkill /f /im %s' % 'py.exe')

class update_file():
    '''文件更新类'''

    def __init__(self):

        # =================================================
        self.server_root_url = "http://106.15.53.80:56789/pyProject/"  # 服务器根目录
        self.local_root_url = "d:/py3flask"  # 本地文件目录
        # =================================================
        self.new_version_number = ""  # 最新版本号(v94)
        self.local_version_number = ""  # 本地版本号(v70)
        # =================================================
        self.server_new_version_url = "http://106.15.53.80:56789/pyProject/newVersion.txt"  # 最新版本号获取地址
        self.local_new_version_url = "d:/py3flask/Version.txt"  # 本地版本号获取地址
        self.local_diary_url = "d:/py3flask/VersionDate.txt"  # 本地日志地址
        # =================================================
        self.new_file_name = ""  # 新版本文件名
        # =================================================
        self.file_download_state = False  # 文件下载状态,默认False
        # =================================================
        self.unfile_status = False  # 文件解压状态
        # =================================================

    # =====================================================
    def get_new_version_number(self):  # 获取新版本号
        '''获取服务器最新版本号'''

        try:
            url = self.server_new_version_url
            r = requests.get(url)
            self.new_version_number = (r.text).lower()
            self.new_file_name = (r.text) + ".zip"
        except:
            print("获取服务器新版本号时失败")

    # =====================================================
    def get_local_version_number(self):  # 获取本地版本号
        '''获取本地版本号'''
        try:
            has_file = os.path.exists(self.local_new_version_url)  # 判断有无此文件
            if has_file:  # 有
                with open(self.local_new_version_url, "r")as f:
                    self.local_version_number = f.read()
            else:  # 没有
                with open(self.local_new_version_url, "w", encoding="utf8")as f:
                    f.write("v1")
        except:
            print('获取本地版本号异常')

    # =====================================================
    def get_file(self):  # 获取新版本的压缩包
        '''下载最新文件并保存'''
        try:
            f = requests.get(self.server_root_url + self.new_file_name)
            with open(self.new_version_number + ".zip", "wb")as n_f:
                n_f.write(f.content)
                self.file_download_state = True
        except:
            print("下载文件错误")

    # =====================================================
    def unzip(self):  # 解压zip文件
        try:
            z = zipfile.ZipFile(self.new_file_name)
            for f in z.namelist():
                z.extract(f, "")
            z.close()
            self.unfile_status = True
        except:
            print("文件解压失败")
    # =====================================================
    def copy_dir(self):

        '''将一个目录下的全部文件和目录,完整地<拷贝并覆盖>到另一个目录'''
        # yuan 源目录
        # target 目标目录

        yuan = self.new_version_number
        target = self.local_root_url
        if not (os.path.isdir(yuan) and os.path.isdir(target)):
            # 如果传进来的不是目录
            print("传入目录不存在")
            return
        try:
            for a in os.walk(yuan):
                # 递归创建目录
                for d in a[1]:
                    dir_path = os.path.join(a[0].replace(yuan, target), d)
                    if not os.path.isdir(dir_path):
                        os.makedirs(dir_path)
                # 递归拷贝文件
                for f in a[2]:
                    dep_path = os.path.join(a[0], f)
                    arr_path = os.path.join(a[0].replace(yuan, target), f)
                    shutil.copy(dep_path, arr_path, follow_symlinks=True)
        except BaseException as e:
            print(e)
            print("覆盖文件时错误")
    # =====================================================
    def write_diray(self):  # 写入日志
        # 写入最新版本号
        with open(self.local_new_version_url, 'w', encoding="utf8")as f:
            f.write(self.new_version_number)
        # 写入更新日志
        has_file = os.path.exists(self.local_diary_url)  # 判断有无此文件
        if has_file:  # 有
            with open(self.local_diary_url, "a", encoding="utf-8")as l:
                time_now = time.strftime("%Y-%m-%d %X", time.localtime())
                version_now = "===Version:" + self.new_version_number
                l.write(time_now + version_now + "\n")
                print("写入更新日志")
                print(time_now)
        else:  # 没有
            with open(self.local_diary_url, "w", encoding="utf8")as n:
                time_now = time.strftime("%Y-%m-%d %X", time.localtime())
                version_now = "===Version:" + self.new_version_number
                n.write(time_now + version_now + "\n")
                print("写入更新日志")
                print(time_now)

    # =====================================================
    def del_file(self):  # 删除多余文件
        try:
            os.remove(self.new_file_name)
            shutil.rmtree(self.new_version_number)
            print("删除多余文件完毕")
        except:
            print("删除文件时候发生错误,文件可能已不存在")

    # =====================================================
    def start_(self, on_off):  # 开启或关闭程序
        if on_off == "open":
            try:
                #creationflags=0x08000000
                subprocess.call('starter.exe', shell=True)
                print("runClient开启")
            except:
                print("关闭runClient时错误")
        elif on_off == "close":
            try:
                subprocess.call('stop.bat', shell=True)
                # subprocess.run("stop.bat")
                print("runClient已关闭")
            except:
                print("关闭runClient时错误")
        else:
            print("传入参数错误")


    # =====================================================
    def main(self):
        while True:
            # 获取服务器最新版本号
            self.get_new_version_number()
            print("最新版本号:", self.new_version_number)
            # 获取当前版本号
            self.get_local_version_number()
            print("当前版本号:", self.local_version_number)

            # 判断一致性
            if self.local_version_number == self.new_version_number:
                print("已是最新版本,不更新")
                print(time.strftime("%Y-%m-%d %X", time.localtime()))
                print("*" * 40)
            else:
                print("线上有最新版,更新")
                self.get_file()
                if self.file_download_state:  # 下载文件成功
                    print("下载文件成功")
                    # 解压文件
                    self.unzip()
                    if self.unfile_status:
                        print("文件解压成功")
                        # # 关闭DS程序
                        self.start_("close")
                        time.sleep(1)  # 给三秒时间关闭
                        # 覆盖文件
                        self.copy_dir()
                        # # 开启DS程序
                        self.start_("open")
                        # 删除多余文件
                        self.del_file()
                        # 写入日志
                        self.write_diray()
                        print("*" * 40)
                    else:
                        print("文件解压失败")
                        return
                else:
                    print("下载文件失败")
                    return
            time.sleep(10)

    def restart_py(self):
        while 1:
            self.start_("close")
            time.sleep(3)
            self.start_("open")
            time.sleep(1800)




if __name__ == "__main__":
    os.system("cls")
    t1 = threading.Thread(target=update_file().main)
    # t2 = threading.Thread(target=update_file().restart_py)
    t1.start()
    # t2.start()
