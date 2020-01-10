#! /usr/bin/env python
# coding:utf-8

import requests, json, os, re, time
from bs4 import BeautifulSoup
from lxml import html
from app.modular.AirLccFareModel import AirRequest, AirLowFareRes, LowFare, DefaultConfig
from app.modular.Segment import Segment
import sys
import logging
# import timeCount

reload(sys)
sys.setdefaultencoding('utf8')

total = 0
success = 0
faild = 0


class Twayair():
    def __init__(self, paramRequest):
        global total
        total+=1
        # 判断传进来的实体是否是AirRequest类生成
        assert isinstance(paramRequest, AirRequest)

        # 定义响应实体
        self.response = AirLowFareRes()
        # 接收请求实体
        self.paramRequest = paramRequest

        # 必要请求参数(用send_parameter方法请求获得)
        self.session = ""
        self._csrf = ""
        self.bt = ""

        #代理ip
        # tunnel_host = "tps136.kdlapi.com"
        # tunnel_port = "15818"
        #
        # tid = "t17793436126235"
        # password = "q3dwz909"
        #
        # self.proxy = {
        #     "http": "http://%s:%s@%s:%s/" % (tid, password, tunnel_host, tunnel_port),
        #     "https": "http://%s:%s@%s:%s/" % (tid, password, tunnel_host, tunnel_port)
        # }
        if self.paramRequest.ip == "" or paramRequest.port == "":
            self.proxy = {}
        else :
            self.proxy = {
                "http": "http://" + paramRequest.ip +":"+paramRequest.port
                ,"https": "https://" +paramRequest.ip +":"+paramRequest.port
            }



        # 出发到达日期人数(send_parameter方法里使用)
        self.go = self.paramRequest.DepAirport
        self.to = self.paramRequest.ArrAirport
        self.date = self.paramRequest.DepDate
        self.AudNum = str(self.paramRequest.AdultNum)
        self.chdNum = str(self.paramRequest.ChildNum)
        # 记录中间页请求成功与否
        self.send_parameter_status = False

        # 回来数据的页面
        self.data_all = ""

    def main(self):

        #计时器/请求时间
        # self.t = timeCount.TimeCount()
        # self.t.start()
        self.t1 = time.time()
        # 拿请求参数

        self.get_parameter()
        # 发送请求参数
        self.send_parameter()
        # 拿数据
        self.get_data()
        # 解析数据
        self.parse_data()

        self.successCount()



        return self.response

    def get_parameter(self):

        # self.t.start() #开始请求计时

        '''请求主页'''
        # ---------------------------------------------------------------
        # 请求报文
        url = "https://www.twayair.com/app/main"
        headers = {
            "Host": "www.twayair.com"
            , "Connection": "keep-alive"
            , "Cache-Control": "max-age=0"
            , "Upgrade-Insecure-Requests": "1"
            , "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                            "Chrome/77.0.3865.120 Safari/537.36 "
            ,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3"
            , "Sec-Fetch-Site": "cross-site"
            , "Accept-Encoding": "gzip, deflate, br"
            , "Accept-Language": "zh-CN,zh;q=0.9"
            , "Cookie": "SETTINGS_REGION=CN; SETTINGS_LANGUAGE=zh-CN;"
        }
        # ---------------------------------------------------------------
        # 发送请求
        try:
            r = requests.get(url=url, headers=headers, proxies=self.proxy)
        except BaseException as e:
            # print e
            self.response.ResultCode = 505
            self.response.Message = "request index exception,proxy error"
            return
        r_text = r.text  # 响应内容
        status_code = r.status_code  # 状态码
        r_text_len = len(r_text)  # 响应内容长度
        # ----------------------------------------------------------------
        # 判断请求
        if r.status_code != 200:
            self.response.ResultCode = 505
            self.response.Message = "request index bad status code:" + str(status_code)
            # print("请求主页失败:",status_code)
            # print("主页响应长度",r_text_len)
            # print("主页内容:",r_text)
            # with open("index_error.html","w",encoding="utf8")as f:
            #     f.write(r_text)
        else:
            # print("请求主页成功:",status_code)
            # print("主页响应长度",r_text_len)
            # -----------------------------------------------------------------
            try:
                # 提取session
                self.session = "SESSION" + re.findall("SESSION(.*?);", str(r.headers))[0] + ";"

                # 提取csrf
                soup = BeautifulSoup(r_text, "html.parser")
                for link in soup.find_all('meta'):
                    if link.get("name") == "_csrf":
                        self._csrf = link.get("content")
                        break

                # 提取bookingticket
                self.bt = re.findall("var _t =(.*?);", r_text)[0].replace(' ', '').replace("'", "")

            except:
                self.response.ResultCode = 500
                self.response.Message = "can't parse parameter"
                # print r.content.decode("utf8")
                return

    def send_parameter(self):
        # self.reqTime = str(self.t.end()) + "s"  # 结束请求计时
        '''请求中间页'''
        # -----------------------------------------------------------------
        # 先判断主页的请求是否成功
        if not self.session:
            # print("主页未请求成功,send_parameter不往下执行")
            return
        # -----------------------------------------------------------------
        # 构造请求报文
        url = "https://www.twayair.com/app/booking/chooseItinerary"
        headers = {
            "Host": "www.twayair.com"
            , "Connection": "keep-alive"
            , "Origin": "https://www.twayair.com"
            , "Cache-Control": "max-age=0"
            , "Upgrade-Insecure-Requests": "1"
            , "Content-Type": "application/x-www-form-urlencoded"
            ,
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36"
            , "Sec-Fetch-Mode": "navigate"
            , "Sec-Fetch-User": "?1"
            ,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3"
            , "Sec-Fetch-Site": "same-origin"
            , "Referer": "https://www.twayair.com/app/main"
            , "Accept-Encoding": "gzip, deflate, br"
            , "Accept-Language": "zh-CN,zh;q=0.9"
            ,
            "Cookie": "_ga=GA1.2.1531734403.1571737546; _gid=GA1.2.375787299.1571737546; SETTINGS_REGION=CN; SETTINGS_LANGUAGE=zh-CN;" + self.session + "SETTINGS_CURRENCY=CNY; wcs_bt=s_12514e83073b:1571737564; __dbl__pv=9; dable_uid=45530640.1571737576840; __ZEHIC7962=1571734155;"
        }

        data = "bookingTicket=" + self.bt
        data += "&tripType=OW"
        data += "&bookingType=HI"
        data += "&promoCodeDetails.promoCode="
        data += "&validPromoCode="
        data += "&availabilitySearches%5B0%5D.depAirport=" + self.go
        data += "&availabilitySearches%5B0%5D.arrAirport=" + self.to
        data += "&availabilitySearches%5B0%5D.flightDate=" + self.date
        data += "&paxCountDetails%5B0%5D.paxCount={}".format(self.AudNum)
        data += "&paxCountDetails%5B1%5D.paxCount={}".format(self.chdNum)
        data += "&paxCountDetails%5B2%5D.paxCount=0"
        data += "&availabilitySearches%5B0%5D.depAirportName="
        data += "&availabilitySearches%5B0%5D.arrAirportName="
        data += "&_csrf=" + self._csrf
        data += "&pax={}".format(self.AudNum)
        data += "&pax={}".format(self.chdNum)
        data += "&pax=0"
        data += "&deptAirportCode=" + self.go
        data += "&arriAirportCode=" + self.to
        data += "&schedule=" + self.date

        # -----------------------------------------------------------------
        # 发送请求
        try:
            r = requests.post(url=url, headers=headers, data=data, proxies=self.proxy)
        except BaseException as e:
            # print("请求中间页异常,可能是代理错误")
            self.response.ResultCode = 505
            self.response.Message = "request middle page exception"
            return
        r_text = r.text  # 响应内容
        r_text_len = len(r_text)  # 响应长度
        status_code = r.status_code  # 状态码

        # -----------------------------------------------------------------
        # 判断响应状况
        if status_code != 200:
            # print("中间页请求失败:",status_code)
            # print("中间页响应体长度:",r_text_len)
            self.response.ResultCode = 505
            self.response.Message = "request middle page bad statu code:" + str(status_code)
            self.send_parameter_status = False
        else:
            # print("中间页请求成功",status_code)
            # print("中间页响应体长度:",r_text_len)
            self.send_parameter_status = True

    def get_data(self):
        # self.reqTime = str(self.t.end()) + "s"  # 结束请求计时
        '''拿数据'''
        # -----------------------------------------------------------------
        # 判断中间请求是否成功
        if not self.send_parameter_status:
            # print("中间页请求未成功,getdata不往下执行")
            return
        # -----------------------------------------------------------------
        # 请求报文
        url = "https://www.twayair.com/app/booking/layerAvailabilityList"
        headers = {
            "Host": "www.twayair.com"
            , "Connection": "keep-alive"
            , "Accept": "text/html, */*; q=0.01"
            , "Origin": "https://www.twayair.com"
            , "X-Requested-With": "XMLHttpRequest"
            ,
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36"
            , "Sec-Fetch-Mode": "cors"
            , "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"
            , "Sec-Fetch-Site": "same-origin"
            , "Referer": "https://www.twayair.com/app/booking/chooseItinerary"
            , "Accept-Encoding": "gzip, deflate, br"
            , "Accept-Language": "zh-CN,zh;q=0.9"
            ,
            "Cookie": "_ga=GA1.2.1531734403.1571737546; _gid=GA1.2.375787299.1571737546; SETTINGS_REGION=CN; SETTINGS_LANGUAGE=zh-CN;" + self.session + "SETTINGS_CURRENCY=CNY; __dbl__pv=9; dable_uid=45530640.1571737576840; __ZEHIC7962=1571734155; wcs_bt=s_12514e83073b:1571737647; _gat_gtag_UA_18196299_2=1; __ZEHIC6330=N; __zjc7702=4937759376; NetFunnel_ID="
        }
        data = "_csrf=" + self._csrf
        # -----------------------------------------------------------------
        # 发送请求
        try:
            r = requests.post(url=url, headers=headers, data=data, proxies=self.proxy)
        except:
            self.response.ResultCode = 500
            self.response.Message = "request data exception"
            # print("请求数据页抛异常,可能是代理错误")
            return
        r_text = r.text  # 响应内容
        r_text_len = len(r_text)  # 响应长度
        status_code = r.status_code  # 状态码
        # -----------------------------------------------------------------
        # 判断请求
        if status_code != 200:
            # print("请求数据页失败:",status_code)
            # print("请求数据页响应长度:",r_text_len)
            self.response.ResultCode = 500
            self.response.Message = "request data bad statu code:" + str(status_code)
        else:
            # print("请求数据页成功:",status_code)
            # print("请求数据页响应长度:",r_text_len)
            self.data_all = r_text
            # 保存html到本地
            # with open("data.html","w") as f:
            #     f.write(r_text)
        # -----------------------------------------------------------------

    def parse_data(self):
        # self.reqTime = str(self.t.end())+"s" #结束请求计时
        # self.t1.start() #开始解析计时
        if self.data_all == "":
            # self.parseTime = str(self.t1.end()) #结束解析计时
            return

        try:
            # with open("data.html","r")as f:
            #     text1 = f.read()
            text1 = self.data_all
            # ==================================================
            # 创建element对象
            html1 = html.etree.HTML(text1)
            #获取航班列表的li标签 element对象组成的list
            airline_list = html1.xpath("//div[@id='price_list_route_1']/ul/li")
            #判断航班条数,为零则返回
            if len(airline_list)==0:
                self.response.Message = "No Data"
                self.response.ResultCode = 404
                return
            #遍历每条航班
            for li in airline_list:

                #每条航班下的盒子列表
                li_box_list = li.xpath("./div/div")
                #遍历每条航班下盒子列表
                for li_box in li_box_list:
                    #一个价格一个实体
                    lf = LowFare()

                    # 针对售罄的判断
                    price = li_box.xpath(".//div[@class='rate_price']/strong/text()")
                    if len(price) != 0:

                        # 先判断有几个航段
                        lf.TripType = 1
                        segs = len(li_box.xpath(".//div[@class='segmentInfo debug']"))
                        # ====2=====
                        lf.ValidatingCarrier = li_box.xpath(".//div[@class='segmentInfo debug']/@data-carriercode")[0]
                        # ====3=====
                        lf.AdultPrice = int(price[0].replace(",", ""))
                        # ====4=====
                        tax1 = int(li_box.xpath(".//div[@class='pricingInfo ADULT']/@data-tax")[0])
                        tax2 = int(li_box.xpath(".//div[@class='pricingInfo ADULT']/@data-surcharge")[0])
                        lf.AdultTax = tax1+tax2
                        # ====5=====
                        lf.TotalPrice = lf.AdultPrice+lf.AdultTax
                        # ====6=====
                        lf.CurrencyCode = li_box.xpath(".//div[@class='pricingInfo ADULT']/@data-currencycode")[0]
                        # ====7=====
                        lf.MaxSeat = li_box.xpath(".//div[@class='rate_price']/span[@class='empty_seats']/text()")[0]
                        lf.MaxSeat = int(re.findall("\d+",lf.MaxSeat)[0])
                        #====航段信息====
                        for segCount in range(segs):
                            seg = Segment()
                            #===============航段数
                            seg.SegmentCount = segCount+1
                            #===============航司名字
                            seg.Carrier = li_box.xpath(".//div[@class='segmentInfo debug']/@data-carriercode")[segCount]
                            # ===============出发机场
                            seg.DepAirport = li_box.xpath(".//div[@class='segmentInfo debug']/@data-departureairportcode")[segCount]
                            # ===============出发时间
                            CfTime = li_box.xpath(".//div[@class='segmentInfo debug']/@data-departuredatetimeltc")[segCount]
                            seg.DepTime = CfTime.replace("T"," ")[0:-3]
                            # ===============到达机场
                            seg.ArrAirport = li_box.xpath(".//div[@class='segmentInfo debug']/@data-arrivalairportcode")[segCount]
                            # ===============到达时间
                            DdTime = li_box.xpath(".//div[@class='segmentInfo debug']/@data-arrivaldatetimeltc")[segCount]
                            seg.ArrTime = DdTime.replace("T", " ")[0:-3]
                            # ===============机型
                            seg.AircraftCode = li_box.xpath(".//div[@class='segmentInfo debug']/@data-aircraftinfotype")[segCount]
                            # ===============航班号
                            seg.FlightNumber = lf.ValidatingCarrier + \
                                               li_box.xpath(".//div[@class='segmentInfo debug']/@data-flightnumber")[segCount]
                            # ===============舱位
                            seg.Cabin = li_box.xpath(".//div[@class='segmentInfo debug']/@data-bookingclass")[segCount][0]
                            # ===============行李额重量
                            seg.BaggageWeigh = li_box.xpath(".//div[@class='ancillary']/@data-exbgsize")[0]
                            if str(seg.BaggageWeigh)=="0":
                                seg.BaggagePiece = ""
                                seg.BaggageWeigh = ""
                            else:
                                seg.BaggagePiece = 1
                            # ===============航段取完,将航段放入LowFare
                            lf.FromSegments.append(seg)
                        # ===============LowFare取完,将LowFare放入AirLowFareRes
                        self.response.LowFareList.append(lf)
                        self.response.Message = "OK"


                        self.response.ResultCode = 200
                        break
                    # else:
                    #     if len(self.response.LowFareList) == 0:
                    #         self.response.Message = "no Data"
                    #         self.response.ResultCode = 404
                    #     else:break

            # self.parseTime = str(self.t1.end()) #结束解析计时

        except:
            self.response.ResultCode = 404
            self.response.Message = "data parse error"
            # self.parseTime = str(self.t1.end()) #结束解析计时

    def successCount(self):
        global success,faild

        if self.response.ResultCode == 200 or self.response.ResultCode == 404:
            success+=1
        else:
            faild +=1

        if DefaultConfig.DEBUG:
            pass
            # print "-" * 80
            # print "(TW) | {}-{} {} | {} | {} | {}s | T:{} | S:{} | F:{} | R:{}".format \
            #     (
            #         self.go,
            #         self.to,
            #         self.date,
            #         self.response.ResultCode,
            #         len(self.response.LowFareList),
            #         round(time.time() - self.t1, 2),
            #         total,
            #         success,
            #         faild,
            #         str(round(float(success) / total * 100, 1)) + "%"
            #     )

if __name__ == "__main__":
    # 模拟一个请求实体a
    a = AirRequest()

    # 赋值请求实体
    a.DepAirport = "NRT"
    a.ArrAirport = "ICN"
    a.DepDate = "2019-12-20"
    a.AdultNum = 4
    a.ChildNum = 0
    #   115.213.175.209:4223
    # a.ip =  "115.213.175.209"
    # a.port = "4223"
    # 声明Tw实体
    s = Twayair(a)

    # 调用Tw实体Main方法
    b = s.main()
    # print b




    # 期望返回的是一个AirLowFareRes实体
    print("*" * 30)