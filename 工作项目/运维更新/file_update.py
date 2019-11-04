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
import time

class update_file():
    '''文件更新类'''
    def __init__(self):

        #=================================================
        self.server_root_url = "http://106.15.53.80:56789/" #服务器根目录
        self.local_root_url = "d:/DirectSpider" #本地文件目录
        #=================================================
        self.new_version_number = "" #最新版本号(v94)
        self.local_version_number = "" #本地版本号(v70)
        #=================================================
        self.server_new_version_url = "http://106.15.53.80:56789/newVersion.txt" #最新版本号获取地址
        self.local_new_version_url = "d:/DirectSpider/Version.txt" #本地版本号获取地址
        self.local_diary_url = "d:/DirectSpider/VersionDate.txt" #本地日志地址
        #=================================================
        self.new_file_name = "" #新版本文件名
        #=================================================
        self.file_download_state = False #文件下载状态,默认False

        self.unfile_status = False #文件解压状态

    #=====================================================
    def get_new_version_number(self): #获取新版本号
        '''获取服务器最新版本号'''

        try:
            url = self.server_new_version_url
            r = requests.get(url)
            self.new_version_number = (r.text).lower()
            self.new_file_name = (r.text)+".zip"
        except:
            print("获取服务器新版本号时失败")
    #===================================================== 
    def get_local_version_number(self): #获取本地版本号
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
    def get_file(self): #获取新版本的压缩包
        '''下载最新文件并保存'''
        try:
            f = requests.get(self.server_root_url+self.new_file_name)
            with open(self.new_version_number+".zip","wb")as n_f:
                n_f.write(f.content)
                self.file_download_state = True
        except:
            print("下载文件错误")
    #=====================================================
    def unzip(self): #解压zip文件
        try:
            z = zipfile.ZipFile(self.new_file_name) 
            for f in z.namelist():
                z.extract(f,"")
            z.close()
            self.unfile_status = True
        except:
            print("文件解压失败")
    #===================================================== 
    def copy_file(self): #覆盖文件
        try:
            for root,dirs,files in os.walk(self.new_version_number,True):
                for eachfile in files:
                    shutil.copy(os.path.join(root,eachfile),self.local_root_url)
        except:
            print("覆盖文件时错误")
    #===================================================== 
    def write_diray(self): #写入日志
        #写入最新版本号
        with open(self.local_new_version_url,'w',encoding="utf8")as f:
            f.write(self.new_version_number)
        #写入更新日志
        has_file = os.path.exists(self.local_diary_url) #判断有无此文件
        if has_file: #有
            with open(self.local_diary_url,"a",encoding="utf-8")as l:
                time_now = time.strftime("%Y-%m-%d %X", time.localtime())
                version_now = "===Version:"+self.new_version_number
                l.write(time_now+version_now+"\n")
                print("写入更新日志")
                print(time_now)
        else: #没有
            with open(self.local_diary_url,"w",encoding="utf8")as n:
                time_now = time.strftime("%Y-%m-%d %X", time.localtime())
                version_now = "===Version:"+self.new_version_number
                n.write(time_now+version_now+"\n")
                print("写入更新日志")
                print(time_now)
    #===================================================== 
    def del_file(self): #删除多余文件
        try:
            os.remove(self.new_file_name)
            shutil.rmtree(self.new_version_number)
            print("删除多余文件完毕")
        except:
            print("删除文件时候发生错误,文件可能已不存在")
    #=====================================================
    def start_(self,on_off): #开启或关闭程序
        if on_off == "open":
            try:
                subprocess.run("start.bat")
                print("DirectSpider开启")
            except:
                print("关闭DirectSpider时错误")
        elif on_off == "close":
            try:
                subprocess.run("stop.bat")
                print("DirectSpider已关闭")
            except:
                print("关闭DirectSpider时错误")
        else:
            print("传入参数错误")
    #=====================================================
    def main(self):
        while True:
            #获取服务器最新版本号
            self.get_new_version_number()
            print("最新版本号:",self.new_version_number)
            #获取当前版本号
            self.get_local_version_number()
            print("当前版本号:",self.local_version_number)

            #判断一致性
            if self.local_version_number == self.new_version_number :
                print("已是最新版本,不更新")
            else:
                print("线上有最新版,更新")
                self.get_file()
                if self.file_download_state:#下载文件成功
                    print("下载文件成功")
                    #解压文件
                    self.unzip()
                    if self.unfile_status:
                        print("文件解压成功")
                        #关闭DS程序
                        self.start_("close")
                        time.sleep(3) #给三秒时间关闭
                        #覆盖文件
                        self.copy_file()
                        #开启DS程序
                        self.start_("open")
                        #写入日志
                        self.write_diray()
                        # 删除多余文件
                        self.del_file()
                    else:
                        print("文件解压失败")
                        return
                else:
                    print("下载文件失败")
                    return
            time.sleep(10)

class send_message():
    #=================================================
    def __init__(self): #初始化
        pass
    #=================================================
    def send(self): #发送数据
        data = {
            'process': self.get_process('Spider.exe'),
            'cpustate': self.get_cpu_state(),
            'memorystate': self.get_memory_state(),
            'computername': self.get_computer_name(),
            'version':self.get_version(),
            'speed':self.get_net_speed()
        }
        # 创建套接字
        udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # 发送数据
        udp_socket.sendto(str(data).encode('utf8'), ('106.15.53.80', 8989))
    #=================================================
    def get_process(self,processname): #获得spider进程数量
        # 检测进程数量
        count = 0
        # 获得一个列表里面存放了所有运行的进程的id
        pl = psutil.pids()
        # 遍历
        try:
            for pid in pl:
                if(psutil.Process(pid).name() == processname):
                    count += 1
            return count
        except:
            get_process(processname)
    #=================================================
    def get_cpu_state(self): #获得CPU使用率
        return str(psutil.cpu_percent(1))
    #=================================================
    def get_memory_state(self): #获得内存使用率
        phymem = psutil.virtual_memory()
        return [phymem.percent, str(int(phymem.used/1024/1024))+"M", str(int(phymem.total/1024/1024))+"M"]
    #=================================================
    def get_computer_name(self): #获得计算机名称
        return socket.gethostname()
    #=================================================
    def get_version(self): #获得Spider本地版本号
        with open("D:/DirectSpider/Version.txt","r")as f:
            return f.read()
    #=================================================
    def get_net_speed(self): #获得过去十秒的平均网速
        #t1时刻发送/接收字节总数
        t1_send = psutil.net_io_counters()[0]
        t1_recv = psutil.net_io_counters()[1]
        
        #等待10秒
        time.sleep(10)
        #t2时刻发送/接收字节总数
        t2_send = psutil.net_io_counters()[0]
        t2_recv = psutil.net_io_counters()[1]
        #t2-t1得到一秒内的上传速率B/S,单位换算Kb/s
        send_end = (t2_send-t1_send)/1000/10
        recv_end = (t2_recv-t1_recv)/1000/10

        up = ["up","%0.1f" % send_end,"kb/s"]
        down = ["down","%0.1f" % recv_end,"kb/s"]
        # print(up)
        # print(down)
        return [up,down]
    #=================================================

    def main(self):
        while True:
            try:
                self.send()
                print("(发送数据)")
            except:
                self.send()

def kill_powershell():
    while True:
        os.system('taskkill /IM cmd.exe /F')
        os.system('taskkill /IM powershell.exe /F')
        time.sleep(57)

    


if __name__ == "__main__":
    os.system("cls")
    t1 = threading.Thread(target=update_file().main)
    t2 = threading.Thread(target=send_message().main)
    t3 = threading.Thread(target=kill_powershell)
    t1.start()
    t2.start()
    t3.start()

