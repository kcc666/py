#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: kcc time:2020/1/17

import socket,time,threading,psutil,os,requests,json,traceback
class Send():
    def __init__(self):

        # 本机项目版本号读取路径
        self.py_version_url = 'd:/py3flask/Version.txt'
        self.csharp_version_url = 'd:/DirectSpider/Version.txt'

        # 本机日志获取路径
        self.log_addr = 'd:/py3flask/log'

        # 本机类型获取路径
        self.host_type_url = "http://106.15.53.80:56789/vpsType.json"


        # 服务器的ip地址
        # self.ip = '106.15.53.80'
        self.ip = '127.0.0.1'
        self.port = 9188

        # 只有连接状态为True时,定时发送基本信息的功能才生效
        self.connectStatus = False

    def main(self):

        # 连接到服务器
        threading.Thread(target=self.connectServer).start()
        # 开启线程定时发送基本信息
        threading.Thread(target=self.sendBasicData).start()
        # 开启线程接收参数并返回日志信息
        threading.Thread(target=self.sendLog).start()





    # 连接器
    def connectServer(self):
        '''连接器,无连接则建立连接,失败则1秒后重试'''

        while 1:
            try:
                # 如果已经建立连接,则continue
                if self.connectStatus: continue

                # 创建套接字
                self.client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

                # 连接到服务器
                self.client.connect((self.ip,self.port))

                # 将连接状态改为已连接
                self.connectStatus = True

            except Exception as e:
                print("连接失败,1秒后重试:"+str(e))
                self.connectStatus = False
                time.sleep(1)

    # -------------服务工具-------------------
    # 在连接状态下,定发送基本信息
    def sendBasicData(self):
        '''连接后发送基本信息'''
        while 1:

            # 判断连接是否还存在
            if not self.connectStatus:
                print("未连接到服务器,不发送数据")
                time.sleep(1);
                continue
            try:
                print("连接存在,准备发送数据")
                self.client.send(self.getBasicData().encode("utf-8"))
                print(time.strftime("%Y-%m-%d %X")+" 发送了一次数据,等待五秒")
                time.sleep(5)
            except Exception as e:
                print(time.strftime("%Y-%m-%d %X")+"|sendBasicData异常:"+str(e))
                if "你的主机中的软件中止了一个已建立的连接" in str(e):self.connectStatus = False
                if "远程主机强迫关闭了一个现有的连接" in str(e): self.connectStatus = False
                time.sleep(1)
    # 根据参数返回日志的服务
    def sendLog(self):
        '''接收到请求后,返回日志信息'''
        while 1:
            # 判断连接是否还存在
            if not self.connectStatus:
                print("未连接到服务器,不启动Log服务")
                time.sleep(1);
                continue
            try:
                recv_msg = self.client.recv(1024).decode("utf8")
                if recv_msg == "dir":
                    print("收到查看日志列表的请求")
                    self.client.send(self.getlog("dir", "").encode("utf8"))
                if recv_msg.startswith("file_"):
                    filename = recv_msg[5:]
                    print("收到查看日志的请求{}".format(filename))
                    self.client.send(self.getlog("file", filename).encode("utf8"))
            except Exception as e:
                # with open("error.txt", "a")as f:
                #     f.write(time.strftime("%Y-%m-%d %X") + "|sendBasic|" + traceback.format_exc().replace("\n", "||")+"\n")
                print(time.strftime("%Y-%m-%d %X")+"|sendLog异常:"+str(e))
                if "你的主机中的软件中止了一个已建立的连接" in str(e): self.connectStatus = False
                if "远程主机强迫关闭了一个现有的连接" in str(e): self.connectStatus = False
                time.sleep(1)

    # ------------本地化工具-------------------
    # 获取日志
    def getlog(self,type,name):
        if type == "dir":
            return json.dumps(os.listdir(self.log_addr))
        if type == "file":
            file_path = os.path.join(self.log_addr,name)
            with open(file_path,"r")as f:
                return f.read()
    # 获取基本信息
    def getBasicData(self):
            '''获得本机信息'''
            result = {
                "type": "你好",
                "py": "NULL",
                "cs": "NULL",
                "cpu": "NULL",
                "memory": "NULL",
                "hostname": "NULL",
                "up": "NULL",
                "down": "NULL",
            }

            # region 本机类型
            r = requests.get(self.host_type_url)
            jsonData = json.loads(r.text)
            for item in jsonData:
                if result['hostname'] == item['computerName']:
                    result["type"] = item["type"]
                    break

            # endregion

            # region python版本
            with open(self.py_version_url, "r")as f:
                result["py"] = f.read()
            # endregion

            # region c#版本
            with open(self.csharp_version_url, "r")as f:
                result["cs"] = f.read()
            # endregion

            # region cpu使用率
            result["cpu"] = psutil.cpu_percent(interval=2)
            # endregion

            # region 内存使用率
            phymem = psutil.virtual_memory()
            m1 = phymem.percent
            m2 = int(phymem.used / 1024 / 1024)
            m3 = int(phymem.total / 1024 / 1024)
            result['memory'] = [m1, m2, m3]
            # endregion

            # region 主机名
            result["hostname"] = os.environ["COMPUTERNAME"]
            # endregion

            # region 网络

            # t1时刻发送/接收字节总数
            t1_send = psutil.net_io_counters()[0]
            t1_recv = psutil.net_io_counters()[1]

            # 等待2秒
            time.sleep(2)
            # t2时刻发送/接收字节总数
            t2_send = psutil.net_io_counters()[0]
            t2_recv = psutil.net_io_counters()[1]
            # t2-t1得到一秒内的上传速率B/S,单位换算Kb/s
            send_end = (t2_send - t1_send) / 1000 / 2
            recv_end = (t2_recv - t1_recv) / 1000 / 2

            up = round(send_end, 1)
            down = round(recv_end, 1)

            result["up"] = up
            result["down"] = down

            # endregion

            return json.dumps(result)



if __name__ == '__main__':
    Send().main()