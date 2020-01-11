# http://139.224.252.126:8066/api/ProxyIP/getip?GetNew=getNew&Operator=100026&InvalidAirlinesID=616&extractCount=1&protocolType=11

import requests,time,json,traceback,re
from lxml import html
requests.packages.urllib3.disable_warnings()
from requests.exceptions import ReadTimeout, ProxyError, ConnectTimeout
from AirLccFareModel import AirRequest, AirLowFareRes, LowFare, DefaultConfig
from requests.exceptions import ReadTimeout, ProxyError, ConnectTimeout
from Segment import Segment

# 测试用的代理IP
def getVpsProxy():
    r = requests.get(
        "http://webapi.http.zhimacangku.com/getip?num=1&type=2&pro=&city=0&yys=0&port=1&time=1&ts=0&ys=0&cs=0&lb=1&sb=0&pb=4&mr=1&regions=")
    jsondata = json.loads(r.text)["data"][0]
    return [str(jsondata["ip"]),str(jsondata["port"])]

class Twayair1():
    def __init__(self,paramRequest):
        # 判断传进来的实体是否是AirRequest类生成
        assert isinstance(paramRequest, AirRequest)

        # 是否打印日志
        self.log = True

        # 是否写HTML到本地
        self.write = True


        # 定义响应实体
        self.response = AirLowFareRes()
        # 接收请求实体
        self.paramRequest = paramRequest
        # 设置超时时间
        self.timeout = 20
        # 代理IP
        self.proxy = {}
        if self.paramRequest.ip and self.paramRequest.port:
            self.proxy = {
                "http": "http://" + paramRequest.ip + ":" + paramRequest.port,
                "https": "https://" + paramRequest.ip + ":" + paramRequest.port
            }
        self.p(self.proxy)






    def main(self):

        #----------------------------------------------------------------------
        # 获取数据
            try:

                searchRes = self.searchFlight()
                self.p(searchRes)

                if searchRes["continue"]:
                    parseRes = self.parseData(searchRes["data"])
                    if parseRes == 404:self.response.ResultCode = 404;self.response.Message = "这条航线无航班"
                    else:self.response.ResultCode = 200;self.response.Message = "成功!"

                else:
                    self.response.ResultCode = 500
                    self.response.Message = "请求数据错误:第{}个请求的状态码是{}".format(searchRes['reqCount'],searchRes['statucode'])

            except ProxyError:
                self.response.ResultCode = 505
                self.response.Message = "无法连接到代理"
            except ConnectTimeout:
                self.response.ResultCode = 507
                self.response.Message = "连接超时:ConnectTimeout"
            except ReadTimeout:
                self.response.ResultCode = 507
                self.response.Message = "读取超时:ReadTimeout"
            except Exception as e:
                self.response.ResultCode = 500
                self.response.Message = "未知原因:"+traceback.format_exc().replace("\n","")

            return self.response
    def p(self,*con):
        '''打印专用'''
        if self.log:
            for i in con:print(i)

    def w(self,filename,con):
        '''写入文件专用'''
        if self.write:
            with open(filename,"wb")as f:
                f.write(con)


    def searchFlight(self):
        '''拿数据'''
        # ----------------------------------------------------------------------------------

        # 本方法的返回结果
        result = {
            "continue":False, # 提示下一个方法是否执行
            "data":"",        # 请求回来的内容
            "statucode":0,    # 请求非200时对应的状态码
            "reqCount":0      # 记录返回时已执行的请求
        }

        # # 请求 1--> 请求头
        headers1 = {
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


        # 请求 1--> 发送请求
        r1  = requests.get(url="https://www.twayair.com/app/main",verify=False ,headers=headers1,timeout=self.timeout,proxies=self.proxy)
        r1_text = r1.text

        # 请求1 --> 保存本地 可注释
        self.w("index.html", r1.content)

        # 请求 1-->非200的返回
        if r1.status_code!=200:
            result = {
                "continue": False,  # 提示下一个方法是否执行
                "data": r1.text,  # 请求回来的内容
                "statucode": r1.status_code,  # 请求对应的状态码
                "reqCount": 1  # 记录返回时已执行的请求
            }

            return result




        # 请求1 --> 获取csrf(本航司必要参数)
        csrf_text = re.findall('<input type="hidden" name="_csrf" value=".*?" />',r1_text)[0]
        csrf_text2 = re.findall('\".*?\"',csrf_text)
        csrf_text3 = csrf_text2[2].replace("\"","")
        # self.p(csrf_text3)


        # 请求1 --> 获取bookingticket(本航司必要参数)
        bookingticket = re.findall("var _t =(.*?);", r1_text)[0].replace(' ', '').replace("'", "")
        # self.p(bookingticket)

        # 请求1 --> 获取session
        session = "SESSION" + re.findall("SESSION(.*?);", str(r1.headers))[0] + ";"
        # self.p(session)
        # ----------------------------------------------------------------------------------
        # 请求2 --> 请求头
        headers2 = {
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
            "Cookie": "_ga=GA1.2.1531734403.1571737546; _gid=GA1.2.375787299.1571737546; SETTINGS_REGION=CN; SETTINGS_LANGUAGE=zh-CN;" + session + "SETTINGS_CURRENCY=CNY; wcs_bt=s_12514e83073b:1571737564; __dbl__pv=9; dable_uid=45530640.1571737576840; __ZEHIC7962=1571734155;"
        }


        # 请求2 --> 请求参数
        data = "bookingTicket=" + bookingticket
        data += "&tripType=OW"
        data += "&bookingType=HI"
        data += "&promoCodeDetails.promoCode="
        data += "&validPromoCode="
        data += "&availabilitySearches%5B0%5D.depAirport=" + self.paramRequest.DepAirport
        data += "&availabilitySearches%5B0%5D.arrAirport=" + self.paramRequest.ArrAirport
        data += "&availabilitySearches%5B0%5D.flightDate=" + self.paramRequest.DepDate
        data += "&paxCountDetails%5B0%5D.paxCount={}".format(self.paramRequest.AdultNum)
        data += "&paxCountDetails%5B1%5D.paxCount={}".format(self.paramRequest.ChildNum)
        data += "&paxCountDetails%5B2%5D.paxCount=0"
        data += "&availabilitySearches%5B0%5D.depAirportName="
        data += "&availabilitySearches%5B0%5D.arrAirportName="
        data += "&_csrf=" + csrf_text3
        data += "&pax={}".format(self.paramRequest.AdultNum)
        data += "&pax={}".format(self.paramRequest.ChildNum)
        data += "&pax=0"
        data += "&deptAirportCode=" + self.paramRequest.DepAirport
        data += "&arriAirportCode=" + self.paramRequest.ArrAirport
        data += "&schedule=" + self.paramRequest.DepDate


        # 请求2 --> 发送请求
        r2 = requests.post(url="https://www.twayair.com/app/booking/chooseItinerary",verify=False, data=data, headers=headers2,timeout=self.timeout,proxies=self.proxy)
        # self.p(r2.status_code)
        if r2.status_code!=200:
            result = {
                "continue": False,  # 提示下一个方法是否执行
                "data": r2.text,  # 请求回来的内容
                "statucode": r2.status_code,  # 请求对应的状态码
                "reqCount": 2  # 记录返回时已执行的请求
            }

            return result

        # ---------------------------------------------------------------------------------
        # 请求3 --> 请求头
        headers3 = {
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
            "Cookie": "_ga=GA1.2.1531734403.1571737546; _gid=GA1.2.375787299.1571737546; SETTINGS_REGION=CN; SETTINGS_LANGUAGE=zh-CN;" + session + "SETTINGS_CURRENCY=CNY; __dbl__pv=9; dable_uid=45530640.1571737576840; __ZEHIC7962=1571734155; wcs_bt=s_12514e83073b:1571737647; _gat_gtag_UA_18196299_2=1; __ZEHIC6330=N; __zjc7702=4937759376; NetFunnel_ID="
        }

        # 请求3 --> 请求参数
        data3 = "_csrf=" + csrf_text3

        # 请求3 --> 发送请求
        r3 = requests.post("https://www.twayair.com/app/booking/layerAvailabilityList",verify=False, data=data3, headers=headers3,timeout=self.timeout,proxies=self.proxy)
        # self.p(r3.status_code)

        # 请求3 --> 写入本地
        self.w("data.html", r3.content)
        if r3.status_code!=200:
            result = {
                "continue": False,  # 提示下一个方法是否执行
                "data": r3.text,  # 请求回来的内容
                "statucode": r3.status_code,  # 请求对应的状态码
                "reqCount": 3  # 记录返回时已执行的请求
            }

            return result


        # ----------------------------------------------------------------------------------
        # 最终返回
        result = {
            "continue": True,  # 提示下一个方法是否执行
            "statucode": r3.status_code,  # 请求对应的状态码
            "reqCount": 3,  # 记录返回时已执行的请求
            "data": r3.text  # 请求回来的内容
        }

        return result

    def parseData(self,con):



        # element对象
        html1 = html.etree.HTML(con)

        # 班次
        airline_list = html1.xpath("//div[@id='price_list_route_1']/ul/li")

        # 如果没数据直接return
        if len(airline_list) == 0:
            return 404

        # 解析
        for li in airline_list:

            # 每条航班下的盒子列表
            li_box_list = li.xpath("./div/div")
            # 遍历每条航班下盒子列表
            for li_box in li_box_list:
                # 一个价格一个实体
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
                    lf.AdultTax = tax1 + tax2
                    # ====5=====
                    lf.TotalPrice = lf.AdultPrice + lf.AdultTax
                    # ====6=====
                    lf.CurrencyCode = li_box.xpath(".//div[@class='pricingInfo ADULT']/@data-currencycode")[0]
                    # ====7=====
                    lf.MaxSeat = li_box.xpath(".//div[@class='rate_price']/span[@class='empty_seats']/text()")[0]
                    lf.MaxSeat = int(re.findall("\d+", lf.MaxSeat)[0])
                    # ====航段信息====
                    for segCount in range(segs):
                        seg = Segment()
                        # ===============航段数
                        seg.SegmentCount = segCount + 1
                        # ===============航司名字
                        seg.Carrier = li_box.xpath(".//div[@class='segmentInfo debug']/@data-carriercode")[segCount]
                        # ===============出发机场
                        seg.DepAirport = li_box.xpath(".//div[@class='segmentInfo debug']/@data-departureairportcode")[
                            segCount]
                        # ===============出发时间
                        CfTime = li_box.xpath(".//div[@class='segmentInfo debug']/@data-departuredatetimeltc")[segCount]
                        seg.DepTime = CfTime.replace("T", " ")[0:-3]
                        # ===============到达机场
                        seg.ArrAirport = li_box.xpath(".//div[@class='segmentInfo debug']/@data-arrivalairportcode")[
                            segCount]
                        # ===============到达时间
                        DdTime = li_box.xpath(".//div[@class='segmentInfo debug']/@data-arrivaldatetimeltc")[segCount]
                        seg.ArrTime = DdTime.replace("T", " ")[0:-3]
                        # ===============机型
                        seg.AircraftCode = li_box.xpath(".//div[@class='segmentInfo debug']/@data-aircraftinfotype")[
                            segCount]
                        # ===============航班号
                        seg.FlightNumber = lf.ValidatingCarrier + \
                                           li_box.xpath(".//div[@class='segmentInfo debug']/@data-flightnumber")[
                                               segCount]
                        # ===============舱位
                        seg.Cabin = li_box.xpath(".//div[@class='segmentInfo debug']/@data-bookingclass")[segCount][0]
                        # ===============行李额重量
                        seg.BaggageWeigh = li_box.xpath(".//div[@class='ancillary']/@data-exbgsize")[0]
                        if str(seg.BaggageWeigh) == "0":
                            seg.BaggagePiece = ""
                            seg.BaggageWeigh = ""
                        else:
                            seg.BaggagePiece = 1
                        # ===============航段取完,将航段放入LowFare
                        lf.FromSegments.append(seg)
                    # ===============LowFare取完,将LowFare放入AirLowFareRes
                    self.response.LowFareList.append(lf)
                    break

        # 如果不抛异常执行到这里,则成功返回
        return 200


if __name__ == '__main__':
    # 模拟一个请求实体a
    a = AirRequest()

    # 赋值请求实体
    a.DepAirport = "NRT"
    a.ArrAirport = "ICN"
    a.DepDate = "2020-01-23"
    a.AdultNum = 1
    a.ChildNum = 0
    ip = getVpsProxy()
    a.ip = ip[0]
    a.port = ip[1]



    s = Twayair1(a)

    # 调用Tw实体Main方法
    b = s.main()
    print(b)