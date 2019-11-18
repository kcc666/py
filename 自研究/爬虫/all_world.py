#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: kcc time:2019/11/16

import requests,re,random,threading,time,os





class SpiderWorld():

    def __init__(self):

        self.headers = {
            "User-Agent":"User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36"
            ,"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3"
        }

        self.timeout = 5

        self.ip_count = 2688889999
        #2642648575
        #4294967295
        self.time_out_count = 0

        self.bad_status_count = 0 

        self.not_title_count = 0 

    def getdata(self,ip):
        
        try:
            r = requests.get(url=ip, headers=self.headers ,timeout=self.timeout)
            r_code = r.status_code
            r_text = r.content.decode("utf8")
            title = re.findall("<title>(.*?)</title>", r_text)

            if r_code!=200: 
                self.bad_status_count+=1
                return
            if len(title)==0:
                self.not_title_count+=1
                return
            if title[0]=="":
                self.not_title_count+=1
                return
            c_ip = ip.replace("http://","")

            with open("f://hello_world/"+c_ip+title[0]+".txt","w",encoding="utf8")as f:
                pass

        except:
            self.time_out_count+=1
            return

    def ipv4(self,n):
        
        if n >= 16777216:
            ip_1 = int(n/16777216)
            ip_1s = n%16777216
            ip_2 = int(ip_1s/65536)
            ip_2s = ip_1s%65536
            ip_3 = int(ip_2s/256)
            ip_3s = ip_2s%256
            ip_4 = ip_3s
            # print(ip_1,ip_2,ip_3,ip_4,sep=".")
            return "{}.{}.{}.{}".format(ip_1,ip_2,ip_3,ip_4)
        elif n<16777216 and n>=65536:
            ip_1 = 0
            ip_2 = int(n/65536)
            ip_2s = n%65536
            ip_3 = int(ip_2s/256)
            ip_3s = ip_2s%256
            ip_4 = ip_3s
            # print(ip_1,ip_2,ip_3,ip_4,sep=".")
            return "{}.{}.{}.{}".format(ip_1,ip_2,ip_3,ip_4)
        elif n<65536 and n>=256:
            ip_1 = 0
            ip_2 = 0
            ip_3 = int(n/256)
            ip_3s = n%256
            ip_4 = ip_3s
            # print(ip_1,ip_2,ip_3,ip_4,sep=".")
            return "{}.{}.{}.{}".format(ip_1,ip_2,ip_3,ip_4)
        else:
            # print("0.0.0.{}".format(n)) 
            return "0.0.0.{}".format(n)

    def main(self):
        while True:
            
            req_ip = "http://"+self.ipv4(self.ip_count)
            self.ip_count-=1
            self.getdata(req_ip)
            
            if self.ip_count<100:return

    def state(self):
        while True:
            with open("a.txt","w",encoding="utf8")as f:
                f.write("当前轮询IP地址{}".format(self.ipv4(self.ip_count))+"\n")
                f.write("当前剩余IP地址数{}".format(self.ip_count)+"\n")
                f.write("超时数量{}".format(self.time_out_count)+"\n")
                f.write("错误状态码数{}".format(self.bad_status_count)+"\n")
                f.write("无效标题数{}".format(self.not_title_count)+"\n")

            time.sleep(10)
            

if __name__ == "__main__":
    a = SpiderWorld()


    for i in range(1000):
        t = threading.Thread(target=a.main)
        t.start()

    a = threading.Thread(target=a.state)
    a.start()

