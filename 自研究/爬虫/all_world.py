#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: kcc time:2019/11/16

import requests,re,random,threading,time,os


def scrapy_ip():
    while True:

        #ip生成器
        ip = str(random.randint(2,254))+"."+str(random.randint(2,254))+"."+str(random.randint(2,254))+"."+str(random.randint(2,254))
        # ip = "162.241.94.119"

        headers = {
            "User-Agent":"User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36"
            ,"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3"
        }
        try:
            r = requests.get("http://"+ip,headers=headers, timeout=5)
            if r.status_code == 200:
                text = r.content.decode("utf8")
                title = re.findall("<title>(.*?)</title>", text)
                if len(title)!=0 :
                    if title[0]!="":
                        print("*" * 40)
                        print(ip)
                        print(title[0])
        except:
            pass

# for i in range(200):
#     t1 = threading.Thread(target=scrapy_ip)
#     t1.start()
# count = 0
# for a in range(0,256):
#     for b in range(0, 256):
#         for c in range(0, 256):
#             for d in range(0, 256):
#                 count+=1
#                 print(a,b,c,d,sep=".")
#                 print(count)
#                 if count == a==1:
#                     time.sleep(1000)

#0.0.0.0
#0

#0.0.1.0
#256

#0.1.0.0
#256*256

#1.0.0.0
#256*256*256
os.system("cls")
print("*"*40)


def ipv4(n):
    n-=1
    if n >= 16777216:
        ip_1 = int(n/16777216)
        ip_1s = n%16777216
        ip_2 = int(ip_1s/65536)
        ip_2s = ip_1s%65536
        ip_3 = int(ip_2s/256)
        ip_3s = ip_2s%256
        ip_4 = ip_3s
        print(ip_1,ip_2,ip_3,ip_4,sep=".")
    elif n<16777216 and n>=65536:
        ip_1 = 0
        ip_2 = int(n/65536)
        ip_2s = n%65536
        ip_3 = int(ip_2s/256)
        ip_3s = ip_2s%256
        ip_4 = ip_3s
        print(ip_1,ip_2,ip_3,ip_4,sep=".")
    elif n<65536 and n>=256:
        ip_1 = 0
        ip_2 = 0
        ip_3 = int(n/256)
        ip_3s = n%256
        ip_4 = ip_3s
        print(ip_1,ip_2,ip_3,ip_4,sep=".")
    else:
        print("0.0.0.{}".format(n))
    




ipv4(257)
print("*"*40)



