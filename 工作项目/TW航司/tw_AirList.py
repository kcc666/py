#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: kcc time:2019/11/29

import requests
import json,time
from lxml import html


# with open("test.csv","ab") as csvfile:
#     writer = csv.writer(csvfile)
#     writer.writerow(["index", "a_name", "b_name"])
#     writer.writerows([[0, 'a1', 'b1']])

class tw_AirList():
    def __init__(self):

        self.headers = {
            "Connection": "keep-alive"
            ,"Accept": "text/html, */*; q=0.01"
            ,"X-Requested-With": "XMLHttpRequest"
            ,"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36"
            ,"Sec-Fetch-Site": "same-origin"
            ,"Sec-Fetch-Mode": "cors"
            ,"Referer": "https://www.twayair.com/app/booking/chooseItinerary"
            ,"Accept-Encoding": "gzip, deflate, br"
            ,"Accept-Language": "zh-CN,zh;q=0.9"
            ,"Cookie": "SETTINGS_REGION=CN; SETTINGS_LANGUAGE=zh-CN; SETTINGS_CURRENCY=CNY;"
        }



    def main(self):

        while 1:
            reqLines = self.readAirLines() #[["ICN","NRT"],["SHE","ICN"]]

            for air in reqLines:
                dep = air[0]
                arr = air[1]
                print (dep,arr,reqLines.index(air))

                try:
                    resultData = self.reqData(dep,arr) #html text
                    parseResult = self.parseData(resultData,dep,arr) #[['2019-11-01', 'not'],['2020-01-23', '956.0']]
                    self.saveData(parseResult)
                except BaseException as e:
                    with open("reqBug.txt", "a")as f:
                        f.write(str(e) + str(time.strftime("%Y-%m-%d %X", time.localtime())) + "\n")
            print("开始等待300秒  ",time.strftime("%Y-%m-%d %X", time.localtime()))
            time.sleep(300)




    def parseData(self,text,dep,arr):

        allDataList = []


        html1 = html.etree.HTML(text)
        dataList = html1.xpath("//div[@data-date_str]")
        # print len(dataList)
        for item in dataList:
            dateLs =  item.xpath("./@data-date_str")
            priceLs =  item.xpath("./@data-fareamt")
            if len(priceLs)==0:
                allDataList.append(["{}-{}".format(dep,arr),dateLs[0],"not"])
            else:
                if priceLs[0]=="0.0":
                    allDataList.append(["{}-{}".format(dep,arr),dateLs[0],"not"])
                else:
                    allDataList.append(["{}-{}".format(dep,arr),dateLs[0], priceLs[0]])
        return allDataList

    def readAirLines(self):

        airLines = []

        with open("airlines.txt","r")as f:
            lines = f.readlines()
            for i in lines:
                d_a = i.replace("\n","")
                dep = d_a.split("-")[0]
                arr = d_a.split("-")[1]
                airLines.append([dep,arr])

        return airLines

    def reqData(self,dep,arr):
        try:
            r = requests.get("https://www.twayair.com/app/layerComponents/scheduleDate/OW/HI/CNY/{}/{}".format(dep, arr),
                             headers=self.headers)
            if r.status_code==200:
                return r.content
            else:
                return "error"
        except:
            return "error"

    def saveData(self,b):

        # 声明数据
        # b = [['OKA-ICN', '2019-11-01', 'not'], ['OKA-ICN', '2019-11-02', 'yes']]

        # 2.读取数据
        with open("test.json","r")as f:
            read = f.read()
            readJson = json.loads(read)


        # 3.准备写入的数据
        for i in b:
            key = i[0]+"|"+i[1]
            val = i[2]
            readJson[key] = val

        # 4.写入数据
        with open("test.json","w")as f:
            f.write(json.dumps(readJson))



if __name__ == '__main__':
    tw_AirList().main()