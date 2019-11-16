#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: kcc time:2019/11/16

import requests,re,random,threading


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
        except BaseException as e:
            pass

for i in range(100):
    t1 = threading.Thread(target=scrapy_ip)
    t1.start()
