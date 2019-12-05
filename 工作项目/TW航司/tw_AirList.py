#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: kcc time:2019/11/29

import requests
import json, time
from lxml import html
import queue
import threading
from flask import Flask, render_template, request

class tw_AirList():
    def __init__(self):


        self.AirLineList = [
            "ICN-FUK", "ICN-HSG", "ICN-KIX", "ICN-KMJ", "ICN-NGO", "ICN-OIT", "ICN-OKA", "ICN-NRT",
            "ICN-RMQ", "ICN-SHE", "ICN-SYX", "ICN-TAO", "ICN-TNA", "ICN-MFM", "ICN-HKG", "ICN-KHH",
            "ICN-WNZ", "ICN-VTE", "ICN-CRK", "ICN-KLO", "ICN-BKK", "ICN-CNX", "ICN-CXR", "ICN-DAD",
            "ICN-HAN", "ICN-SGN", "ICN-GUM", "ICN-SPN", "GMP-CJU", "GMP-TSA", "CJU-GMP", "CJU-TAE",
            "CJU-KWJ", "CJU-MWX", "CJU-NGO", "CJU-NRT", "CJU-KIX", "CJU-TPE", "CJU-TSA", "CJU-HKG",
            "CJU-DYG", "CJU-YNJ", "CJU-CEB", "CJU-KLO", "CJU-BKK", "CJU-CXR", "CJU-DAD", "CJU-HAN",
            "CJU-GUM", "TAE-CJU", "TAE-OKA", "TAE-NRT", "TAE-KIX", "TAE-FUK", "TAE-TPE", "TAE-HKG",
            "TAE-DYG", "TAE-YNJ", "TAE-CEB", "TAE-KLO", "TAE-BKK", "TAE-CXR", "TAE-DAD", "TAE-HAN",
            "TAE-GUM", "PUS-KIX", "PUS-KHH", "PUS-RMQ", "PUS-TPE", "PUS-DAD", "PUS-HAN", "PUS-VTE",
            "MWX-CJU", "KWJ-CJU", "KWJ-KIX", "KWJ-NRT", "OKA-ICN", "OKA-TAE", "OKA-RMQ", "OKA-KHH",
            "OKA-BKK", "OKA-SGN", "OKA-KLO", "OKA-HAN", "OKA-DAD", "OKA-CXR", "OKA-CEB", "OKA-VTE",
            "OKA-GUM", "OKA-SPN", "OIT-ICN", "OIT-RMQ", "OIT-KHH", "OIT-SGN", "OIT-KLO", "OIT-BKK",
            "OIT-HAN", "OIT-DAD", "OIT-CXR", "OIT-CRK", "OIT-CEB", "OIT-VTE", "OIT-GUM", "OIT-SPN",
            "NRT-ICN", "NRT-CJU", "NRT-TAE", "NRT-KWJ", "NRT-RMQ", "NRT-KHH", "NRT-VTE", "NRT-CEB",
            "NRT-KLO", "NRT-BKK", "NRT-CXR", "NRT-DAD", "NRT-HAN", "NRT-SGN", "NRT-GUM", "NRT-SPN", "NGO-ICN",
            "NGO-CJU", "NGO-RMQ", "NGO-KHH", "NGO-SGN", "NGO-KLO", "NGO-BKK", "NGO-HAN", "NGO-DAD", "NGO-CXR",
            "NGO-VTE", "NGO-GUM", "NGO-SPN", "CTS-RMQ", "CTS-KHH", "CTS-BKK", "CTS-SGN", "CTS-KLO", "CTS-HAN",
            "CTS-DAD", "CTS-CXR", "CTS-CEB", "CTS-VTE", "CTS-GUM", "CTS-SPN", "FUK-ICN", "FUK-TAE", "FUK-RMQ",
            "FUK-KHH", "FUK-BKK", "FUK-SGN", "FUK-KLO", "FUK-HAN", "FUK-DAD", "FUK-CXR", "FUK-CRK", "FUK-VTE",
            "FUK-GUM", "FUK-SPN", "HSG-ICN", "HSG-RMQ", "HSG-KHH", "HSG-SGN", "HSG-KLO", "HSG-BKK", "HSG-HAN",
            "HSG-DAD", "HSG-CXR", "HSG-CRK", "HSG-CEB", "HSG-VTE", "HSG-GUM", "HSG-SPN", "KIX-ICN", "KIX-CJU",
            "KIX-TAE", "KIX-KWJ", "KIX-PUS", "KIX-RMQ", "KIX-KHH", "KIX-VTE", "KIX-CEB", "KIX-KLO", "KIX-BKK",
            "KIX-CXR", "KIX-DAD", "KIX-HAN", "KIX-SGN", "KIX-GUM", "KIX-SPN", "KMJ-ICN", "KMJ-RMQ", "KMJ-KHH",
            "KMJ-SGN", "KMJ-KLO", "KMJ-BKK", "KMJ-HAN", "KMJ-DAD", "KMJ-CXR", "KMJ-CRK", "KMJ-CEB", "KMJ-VTE",
            "KMJ-GUM", "KMJ-SPN", "KOJ-RMQ", "KOJ-KHH", "KOJ-BKK", "KOJ-SGN", "KOJ-KLO", "KOJ-HAN", "KOJ-DAD",
            "KOJ-CXR", "KOJ-CRK", "KOJ-CEB", "KOJ-VTE", "KOJ-GUM", "KOJ-SPN", "RMQ-ICN", "RMQ-PUS", "RMQ-CTS",
            "RMQ-OKA", "RMQ-OIT", "RMQ-NRT", "RMQ-NGO", "RMQ-KOJ", "RMQ-KMJ", "RMQ-KIX", "RMQ-HSG", "RMQ-FUK",
            "RMQ-GUM", "RMQ-SPN", "SHE-ICN", "YNJ-CJU", "YNJ-TAE", "WNZ-ICN", "WNZ-SPN", "TSA-GMP", "TSA-CJU",
            "TPE-CJU", "TPE-TAE", "TPE-PUS", "TNA-ICN", "TNA-CTS", "TNA-OKA", "TNA-OIT", "TNA-NRT", "TNA-NGO",
            "TNA-KOJ", "TNA-KMJ", "TNA-KIX", "TNA-HSG", "TNA-FUK", "TNA-SPN", "TAO-ICN", "SYX-ICN", "MFM-ICN",
            "DYG-CJU", "DYG-TAE", "HKG-ICN", "HKG-CJU", "HKG-TAE", "KHH-ICN", "KHH-PUS", "KHH-CTS", "KHH-OKA",
            "KHH-OIT", "KHH-NRT", "KHH-NGO", "KHH-KOJ", "KHH-KMJ", "KHH-KIX", "KHH-HSG", "KHH-FUK", "KHH-GUM",
            "KHH-SPN", "SGN-ICN", "SGN-CTS", "SGN-OIT", "SGN-NRT", "SGN-NGO", "SGN-KOJ", "SGN-KMJ", "SGN-KIX",
            "SGN-HSG", "SGN-FUK", "SGN-OKA", "VTE-ICN", "VTE-PUS", "CNX-ICN", "CRK-ICN", "CXR-ICN", "CXR-CJU",
            "CXR-TAE", "CXR-HSG", "CXR-OKA", "CXR-OIT", "CXR-NRT", "CXR-NGO", "CXR-KOJ", "CXR-CTS", "CXR-KIX",
            "CXR-FUK", "CXR-KMJ", "DAD-ICN", "DAD-CJU", "DAD-TAE", "DAD-PUS", "DAD-HSG", "DAD-OKA", "DAD-OIT",
            "DAD-NRT", "DAD-NGO", "DAD-CTS", "DAD-KMJ", "DAD-KIX", "DAD-FUK", "DAD-KOJ", "BKK-ICN", "BKK-CJU",
            "BKK-TAE", "BKK-HSG", "BKK-OKA", "BKK-OIT", "BKK-NRT", "BKK-NGO", "BKK-KOJ", "BKK-CTS", "BKK-KIX",
            "BKK-FUK", "BKK-KMJ", "HAN-ICN", "HAN-CJU", "HAN-TAE", "HAN-PUS", "HAN-HSG", "HAN-OKA", "HAN-OIT",
            "HAN-NRT", "HAN-NGO", "HAN-CTS", "HAN-KMJ", "HAN-KIX", "HAN-FUK", "HAN-KOJ", "KLO-ICN", "KLO-CJU",
            "KLO-TAE", "CEB-CJU", "CEB-TAE", "SPN-ICN", "GUM-ICN", "GUM-CJU", "GUM-TAE", "GUM-KIX", "GUM-NGO",
        ]
        self.q = queue.Queue()
        for i in self.AirLineList:
            self.q.put(i)



        self.dataAllDict = {}

    def main(self):

        while 1:
            if self.q.empty():
                print("任务队列已空,本线程结束")
                return
            dep_arr = self.q.get_nowait()
            dep = dep_arr.split("-")[0]
            arr = dep_arr.split("-")[1]
            print("执行{},队列剩余数量{}".format(dep_arr,self.q.qsize()))
            reqText = self.reqData(dep,arr)
            # if reqText == "error":
            #     print("本次任务执行失败{},重新回归队列".format(dep_arr))
            #     self.q.put_nowait(dep_arr)
            #     continue
            parData = self.parseData(reqText,dep,arr)
            self.saveDict(parData)
            print(len(self.dataAllDict))

    def parseData(self, text, dep, arr):

        allDataList = []

        html1 = html.etree.HTML(text)
        dataList = html1.xpath("//div[@data-date_str]")
        # print len(dataList)
        for item in dataList:
            dateLs = item.xpath("./@data-date_str")
            priceLs = item.xpath("./@data-fareamt")
            if len(priceLs) == 0:
                allDataList.append(["{}-{}".format(dep, arr), dateLs[0], "not"])
            else:
                if priceLs[0] == "0.0":
                    allDataList.append(["{}-{}".format(dep, arr), dateLs[0], "not"])
                else:
                    allDataList.append(["{}-{}".format(dep, arr), dateLs[0], priceLs[0]])
        return allDataList

    def reqData(self,dep,arr):

        proxy = {
            "http": "http://58.19.82.214:4228"
            , "https": "https://58.19.82.214:4228"
        }
        headers = {
            "Connection": "keep-alive"
            , "Accept": "text/html, */*; q=0.01"
            , "X-Requested-With": "XMLHttpRequest"
            ,
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36"
            , "Sec-Fetch-Site": "same-origin"
            , "Sec-Fetch-Mode": "cors"
            , "Referer": "https://www.twayair.com/app/booking/chooseItinerary"
            , "Accept-Encoding": "gzip, deflate, br"
            , "Accept-Language": "zh-CN,zh;q=0.9"
            , "Cookie": "SETTINGS_REGION=CN; SETTINGS_LANGUAGE=zh-CN; SETTINGS_CURRENCY=CNY;"
        }

        try:
            r = requests.get(
                "https://www.twayair.com/app/layerComponents/scheduleDate/OW/HI/CNY/{}/{}".format(dep, arr),headers=headers)
            if r.status_code == 200:
                return r.content
            else:
                with open("errorLog.txt","a",encoding='utf8')as f:
                    f.write(str(r.status_code)+"|"+time.strftime("%Y-%m-%d %X",time.localtime())+"\n")
                return "error"
        except BaseException as e:
            with open("errorLog.txt", "a",encoding='utf8')as f:
                f.write(str(e) + "|" + time.strftime("%Y-%m-%d %X",time.localtime())+"\n")
            return "error"

    def saveDict(self,d):
        for i in d:
            key = "{}|{}".format(i[0],i[1])
            val = i[2]
            self.dataAllDict[key] = val


if __name__ == '__main__':

    a = tw_AirList() #新建类

    app = Flask(__name__)

    @app.route('/search')
    def recvGet():
        try:
            condition = request.args.get('q')
            return a.dataAllDict[condition]
        except:
            return "notfound"

    # app.run(debug=True, host='127.0.0.1', port=8081)

    t1 = threading.Thread(target=app.run,args=('0.0.0.0',8318))
    t1.start()

    while 1:
        tlist = [] #线程池
        for i in range(30):
            t1 = threading.Thread(target=a.main)
            t1.start()
            tlist.append(t1)

        for j in tlist:
            j.join()
        print("本次数据抓取完毕,等待300秒重新抓取")
        time.sleep(300)
        for i in a.AirLineList:
            a.q.put(i)

