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
import traceback

lock = threading.Lock()

class send_status():
    def __init__(self):
        pass
    def main(self):
        while 1:
            try:
                self.send()
            except Exception as e:
                print(e)
                time.sleep(10)
    # 获得计算机名称
    def get_cpn(self):
        return os.environ["COMPUTERNAME"]
    # 获得CPU使用率
    def get_cpu(self):
        cp = psutil.cpu_percent(interval=7, percpu=False)
        return cp
    # 获得内存使用率
    def get_memory(self):
        phymem = psutil.virtual_memory()
        m1 = phymem.percent
        m2 = int(phymem.used / 1024 / 1024)
        m3 = int(phymem.total / 1024 / 1024)
        return [m1,m2,m3]
    # 获得网络使用率
    def get_net(self):
        # t1时刻发送/接收字节总数
        t1_send = psutil.net_io_counters()[0]
        t1_recv = psutil.net_io_counters()[1]

        # 等待10秒
        time.sleep(2)
        # t2时刻发送/接收字节总数
        t2_send = psutil.net_io_counters()[0]
        t2_recv = psutil.net_io_counters()[1]
        # t2-t1得到一秒内的上传速率B/S,单位换算Kb/s
        send_end = (t2_send - t1_send) / 1000 / 2
        recv_end = (t2_recv - t1_recv) / 1000 / 2

        up = round(send_end, 2)
        down = round(recv_end, 2)
        return [up,down]
    # 获得本机类型
    def get_type(self):
        try:
            r = requests.get("http://106.15.53.80:56789/vpsType.json",timeout=10)
            r_text = r.text
            a = json.loads(r_text)
            cpn = self.get_cpn()
            for i in a:
                if i["computerName"] == cpn:
                    return i["type"]
            return "unknown"
        except Exception as e:
            print(e)
            return "error"
    # 获得本地版本
    def get_version(self):

        with open("D:/DirectSpider/Version.txt", "r")as f:
            csv = f.read()
        with open("D:/py3flask/Version.txt", "r")as f1:
            pyv = f1.read()

        return [csv,pyv]
    def send(self):

        cpn = self.get_cpn()
        cpu = self.get_cpu()
        m = self.get_memory()
        m1 = m[0]
        m2 = m[1]
        m3 = m[2]
        net = self.get_net()
        up = net[0]
        down = net[1]
        ctype = self.get_type()
        v = self.get_version()
        csv= v[0]
        pyv= v[1]


        param = {
            "cpn":cpn,
            "cpu":cpu,
            "cpu":cpu,
            "m1":m1,
            "m2":m2,
            "m3":m3,
            "up":up,
            "down":down,
            "type":ctype,
            "pyv":pyv,
            "csv":csv
        }

        requests.get('http://106.15.53.80:7001', params=param, timeout=10)

        # 3.
        global lock
        lock.acquire()
        print(time.strftime("%Y-%m-%d %X") + "----发送数据")
        lock.release()

py = {
    "新版本号路径":"http://106.15.53.80:56789/pyProject/newVersion.txt",
    "老版本号路径":"D:\py3flask\Version.txt",
    "日志路径": "D:\py3flask\VersionDate.txt",
    "新版本号:":"" ,
    "老版本号":"",
    "新版本下载地址":""
}


cs = {
    "新版本号路径":"http://106.15.53.80:56789/newVersion.txt",
    "老版本号路径":"D:\DirectSpider\Version.txt",
    "日志路径": "D:\DirectSpider\VersionDate.txt",
    "新版本号:":"" ,
    "老版本号":"",
    "新版本下载地址":""
}

def 获取新版本号(新版本路径):
    a = requests.get(新版本路径,timeout=5)
    return a.text

def 获取老版本号(老版本路径):
    with open(老版本路径,"r")as f:
        return f.read()

def 下载文件(新版本下载地址,新版本存放地址):
    # 文件存放地址

    f = requests.get(新版本下载地址,timeout=30,stream=True)
    with open(新版本存放地址, "wb")as n_f:
        n_f.write(f.content)

def 解压文件(文件路径,解压地址):
    z = zipfile.ZipFile(文件路径)
    for f in z.namelist():
        # print(os.path.split(py["老版本号路径"])[0]+"/"+f)
        z.extract(f, 解压地址)
    z.close()

def 关闭程序(项目):
    subprocess.call('stop{}.bat'.format(项目), shell=True)

def 开启程序(项目):
    subprocess.call('start{}.exe'.format(项目), shell=True)
    if 项目=="cs":subprocess.call('start{}.bat'.format(项目), shell=True)

def 覆盖文件(yuan,target):
    '''将一个目录下的全部文件和目录,完整地<拷贝并覆盖>到另一个目录'''
    # yuan 源目录
    # target 目标目录
    if not (os.path.isdir(yuan) and os.path.isdir(target)):
        # 如果传进来的不是目录
        print("传入目录不存在")
        return

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

def 删除文件(目录,文件):
    shutil.rmtree(目录)
    os.remove(文件)

def 记录日志(日志路径,新版本号,老版本号路径):
    with open(日志路径,"a")as f:
        version_now = "===Version:" + 新版本号
        f.write(time.strftime("%Y-%m-%d %X")+version_now+"\n")
    with open(老版本号路径,"w")as f:
        f.write(新版本号)

def kill_powershell():
    global lock
    while True:
        try:
            subprocess.call('taskkill /F /IM powershell.exe', creationflags=0x08000000, shell=True)
            # 1.
            lock.acquire()
            print(time.strftime("%Y-%m-%d %X")+"----Kill PowerShell")
            lock.release()
            time.sleep(30)
        except:

            time.sleep(57)


def 项目更新(信息,项目名):
    global lock
    while True:
        try:
            # 获取最新版本号
            信息["新版本号"] = 获取新版本号(信息["新版本号路径"])

            # 获取本地版本号
            信息["老版本号"] = 获取老版本号(信息["老版本号路径"])
            # 2.

            lock.acquire()
            print(time.strftime("%Y-%m-%d %X")+"-{}-最新:{}当前:{}".format(项目名,信息["新版本号"],信息["老版本号"]))
            lock.release()
            if 信息["老版本号"] != 信息["新版本号"]:

                信息["新版本下载地址"] = os.path.split(信息["新版本号路径"])[0] + "/" + 信息["新版本号"] + ".zip"
                新版本存放地址 = os.path.split(信息["老版本号路径"])[0] + "/" + 信息["新版本号"] + ".zip"
                下载文件(信息["新版本下载地址"], 新版本存放地址)

                解压地址 = os.path.split(信息["老版本号路径"])[0]

                解压文件(新版本存放地址,解压地址)
                关闭程序(项目名)
                覆盖文件(新版本存放地址.replace('.zip', ""), os.path.split(信息["老版本号路径"])[0])
                开启程序(项目名)
                删除文件(新版本存放地址.replace('.zip', ""), 新版本存放地址)
                记录日志(信息["日志路径"], 信息["新版本号"], 信息["老版本号路径"])
            time.sleep(10)
        except Exception as e:
            with open("Error.txt","a")as f:
                f.write(time.strftime("%Y-%m-%d %X")+"-{}-".format(项目名)+traceback.format_exc().replace("\n","AAAA")+"\n")
            time.sleep(5)



if __name__ == '__main__':
    # 程序开始
    # cs更新()
    # py更新()

    t1 = threading.Thread(target=项目更新,args=(py,"py"))
    t2 = threading.Thread(target=项目更新,args=(cs,"cs"))
    t3 = threading.Thread(target=kill_powershell)
    t4 = threading.Thread(target=send_status().main)

    t1.start()
    t2.start()
    t3.start()
    t4.start()
