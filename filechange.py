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
#服务器地址
server_path = "http://106.15.53.80:56789/"
#本地路径
local_path = "d://DirectSpider/"
#文件格式
file_format = ".zip"
#新版本号路径
new_version_path = server_path+'newVersion.txt'
#当前版本号路径
current_version_path = local_path+"Version.txt"
#新文件下载路径
new_version_file = ""
#新文件名
new_file_name = ""
#解压后目录名
unzip_dir_name = ""
#更新日志路径
log_path = local_path+"VersionDate.txt"


#获取新版本号
def get_new_version():
    '''获取最新版版本号'''
    global new_version_file
    global new_file_name
    global unzip_dir_name
    try:
        r = requests.get(new_version_path)
        new_vs = r.text.lower()
        new_version_file = server_path+new_vs+file_format
        new_file_name = new_vs+file_format
        unzip_dir_name = new_vs
        print("最新版本号:",new_vs)
        return new_vs 
    except:
        print("获取最新版本号失败")
        return "f"
#获取当前版本号
def get_current_version():
    '''获取本地路径最新版本号'''

    try:
        hasfile = os.path.exists(current_version_path)
        if hasfile:
            with open(current_version_path,"r",encoding="utf-8")as f:
                current_vs = f.read().lower()
                print("本地版本号:",current_vs)
                return current_vs
        else:
            with open(current_version_path,"w",encoding="utf-8")as f:
                f.write("新创建该文件")
                
    except:
        print("获取本地版本号失败")
        return "f"
#下载最新文件
def get_new_file():
    '''下载文件并保存,目录为local_path'''
    try:
        f =  requests.get(new_version_file)
        with open(local_path+new_file_name,"wb")as n_f:
            n_f.write(f.content)
            print("下载文件成功")
    except:
        print("下载文件错误")
        return "f"
#解压文件
def unzip():
    try:
        zipFile = zipfile.ZipFile(local_path+new_file_name)
        for file in zipFile.namelist():
            zipFile.extract(file,local_path)
        zipFile.close()
        print("文件解压成功")
    except:
        return "f"
#关闭DS程序
def close_ds():
    try:
        subprocess.run("stop.bat",shell=True)
        print("DirectSpider已关闭")
        time.sleep(3)
    except:
        print("关闭DirectSpider时错误")
        return "f"
#覆盖新文件
def copy_file():
    try:
        for root,dirs,files in os.walk(local_path+unzip_dir_name,True):
            for eachfile in files:
                shutil.copy(os.path.join(root,eachfile),local_path)
        print("文件覆盖成功")
    except:
        print("覆盖文件时错误")
        return "f"
#开启DS程序
def run_ds():
    try:
        time.sleep(3)
        subprocess.run("start.bat",shell=True)
        print("DirectSpider已开启")
    except:
        print("开启DirectSpider时错误")
        return "f"
#删除多余文件
def del_file():
    try:
        os.remove(local_path+new_file_name)
        shutil.rmtree(local_path+unzip_dir_name)
        print("删除多余文件完毕")
    except:
        print("删除文件时候发生错误,文件可能已不存在")
        return "f"
#更新日志
def up_log():
    try:
        with open(current_version_path,"w",encoding="utf-8")as f:
            f.write(unzip_dir_name)
            
        with open(log_path,"a",encoding="utf-8")as l:
            time_now = time.strftime("%Y-%m-%d %X", time.localtime())
            version_now = "===Version:"+unzip_dir_name
            l.write(time_now+version_now+"\n")
        print("写入更新日志")
        print(time_now)
    except:
        print("更新日志时发生错误")
        return "f"


#文件更新
def filechange():
    while True:
        print("--"*20)
        print("等待10秒检测更新")
        time.sleep(10)

        #最新版本号
        n = get_new_version()
        if n == "f":
            continue
        #获取当前版本号
        c = get_current_version()
        if c == "f":
            continue
        #比对两个版本号是否一致
        if c==n:
            #版本号一致,不做修改
            print("版本号一致,不做修改")
            print(time.strftime("%Y-%m-%d %X", time.localtime()))
            continue
        else:
            #版本号不一致
            print("发现新版本"+unzip_dir_name+",准备更新")
            #下载最新版本号
            if get_new_file() == "f":
                continue
            #解压到本地目录
            if unzip() == "f":
                continue
            #关闭DS程序,等待5秒
            if close_ds() == "f":
                continue
            #将解压得到的文件夹里的文件覆盖到DS目录
            if copy_file() == "f":
                continue
            #开启DS程序
            if run_ds() == "f":
                continue
            #删除多余文件
            if del_file() == "f":
                continue
            #写入更新记录
            if up_log() == "f":
                continue

def kill_powershell():
    while True:
        os.system('taskkill /IM powershell.exe /F')
        time.sleep(60)
    

    
    

if __name__ == "__main__":
    #清屏
    os.system("cls")
    #文件更新
    t1 = threading.Thread(target=filechange)
    #发送当前数据
    t2 = threading.Thread(target=sendMessage.main)
    #终止powershell
    t3 = threading.Thread(target=kill_powershell)


    t1.start()
    t2.start()
    t3.start()

    t1.join()
    t2.join()
    t3.join()
