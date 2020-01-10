# http://139.224.252.126:8066/api/ProxyIP/getip?GetNew=getNew&Operator=100026&InvalidAirlinesID=616&extractCount=1&protocolType=11

import requests,time,json,traceback,re
requests.packages.urllib3.disable_warnings()
from AirLccFareModel import AirRequest, AirLowFareRes, LowFare, DefaultConfig
from requests.exceptions import ReadTimeout, ProxyError, ConnectTimeout


# 测试用的代理IP
def getVpsProxy():
    r = requests.get(
        "http://139.224.252.126:8066/api/ProxyIP/getip?GetNew=getNew&Operator=100026&InvalidAirlinesID=616&extractCount=1&protocolType=11")
    ip = eval(json.loads(r.text))[0]
    return ip.split(":")

class Twayair1():
    def __init__(self,paramRequest):
        # 判断传进来的实体是否是AirRequest类生成
        assert isinstance(paramRequest, AirRequest)

        # 是否打印日志
        self.log = True
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
            except Exception as e:
                print(traceback.format_exc(1))

    def p(self,*con):
        '''打印专用'''
        if self.log:
            for i in con:print(i)


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

        # 请求 1-->非200的返回
        if r1.status_code!=200:
            result = {
                "continue": False,  # 提示下一个方法是否执行
                "data": r1.text,  # 请求回来的内容
                "statucode": r1.status_code,  # 请求对应的状态码
                "reqCount": 1  # 记录返回时已执行的请求
            }

            return result

        # 请求1 --> 保存本地 可注释
        with open("index.html","wb")as f:
            f.write(r1.content)
            self.p("成功写入文件")


        # 请求1 --> 获取csrf(本航司必要参数)
        csrf_text = re.findall('<input type="hidden" name="_csrf" value=".*?" />',r1_text)[0]
        csrf_text2 = re.findall('\".*?\"',csrf_text)
        csrf_text3 = csrf_text2[2].replace("\"","")
        self.p(csrf_text3)


        # 请求1 --> 获取bookingticket(本航司必要参数)
        bookingticket = re.findall("var _t =(.*?);", r1_text)[0].replace(' ', '').replace("'", "")
        self.p(bookingticket)

        # 请求1 --> 获取session
        session = "SESSION" + re.findall("SESSION(.*?);", str(r1.headers))[0] + ";"
        self.p(session)
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
        self.p(r2.status_code)
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
        self.p(r3.status_code)
        if r3.status_code!=200:
            result = {
                "continue": False,  # 提示下一个方法是否执行
                "data": r3.text,  # 请求回来的内容
                "statucode": r3.status_code,  # 请求对应的状态码
                "reqCount": 3  # 记录返回时已执行的请求
            }

            return result
        # 请求3写入本地,可注释
        with open("data.html","wb")as f:
            f.write(r3.content)
            self.p("写入文件完毕")
        # ----------------------------------------------------------------------------------
        # 最终返回
        result = {
            "continue": True,  # 提示下一个方法是否执行
            "statucode": r3.status_code,  # 请求对应的状态码
            "reqCount": 3,  # 记录返回时已执行的请求
            "data": r3.text  # 请求回来的内容
        }

        return result



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
