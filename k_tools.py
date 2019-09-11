import time
import psutil
import os
import socket
import requests
import zipfile
import threading

def time_now():
    '''(str),获取当前时间:年-月-日 时分秒'''
    return time.strftime("%Y-%m-%d %X", time.localtime())

def get_cpu_state():
    '''(str),获取cpu使用率'''
    return str(psutil.cpu_percent(1))

def get_process(processname):
    '''(int),传入进程名,返回该进程运行数量'''
    count = 0
    pl = psutil.pids()
    try:
        for pid in pl:
            if(psutil.Process(pid).name() == processname):
                count += 1
        return count
    except:
        get_process(processname)

def clear_console():
    '''清空控制台'''
    os.system('cls')

def get_memory_state():
    '''(List),返回内存使用情况'''
    phymem = psutil.virtual_memory()
    return [phymem.percent, str(int(phymem.used/1024/1024))+"M", str(int(phymem.total/1024/1024))+"M"]


def get_computer_name():
    '''(str)返回当前计算机名'''
    return socket.gethostname()

def extract_zip(file_dir):
    zipFile = zipfile.ZipFile(file_dir)
    for file in zipFile.namelist():
        zipFile.extract(file, r'C:\Users\46321\Desktop\Kcc备份\py\zip')
    zipFile.close()

def down_file(from_url, to_url):
    '''(下载地址,保存地址)下载文件'''
    try:
        response = requests.get(from_url)
        with open(to_url, 'wb')as f:
            f.write(response.content)
    except BaseException as e:
        print(e)
        print('下载文件时发生错误')

def run_app(addr):
    '''(程序地址)打开程序'''
    os.system()

def timer_run(timer_start_time, func):
    '''(时间,方法),多少秒后执行某方法'''
    timer = threading.Timer(timer_start_time, func)
    timer.start()



