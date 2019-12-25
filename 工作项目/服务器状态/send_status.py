#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: kcc time:2019/12/25

import requests,psutil,os,time,json


class send_status():
    def __init__(self):
        pass
    def main(self):
        while 1:
            self.send()
            time.sleep(5)
    # 获得计算机名称
    def get_cpn(self):
        return os.environ["COMPUTERNAME"]

    # 获得CPU使用率
    def get_cpu(self):
        return psutil.cpu_percent(2)

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
            r = requests.get("http://106.15.53.80:56789/vpsType.json")
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
        with open("D:/hmyd_flask_scrapy/Version.txt", "r")as f1:
            pyv = f1.read()

        return [csv,pyv]

    def send(self):

        try:
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

            requests.get('http://106.15.53.80:7001', params=param)
            print("发送数据",time.strftime("%Y-%m-%d %X"))

        except Exception as e:
            with open("except.txt","a")as f:
                f.write(time.strftime("%Y-%m-%d %X")+"|"+str(e)+"\n")



if __name__ == '__main__':
    send_status().main()

