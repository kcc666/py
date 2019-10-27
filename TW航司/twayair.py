import requests,json,os,re,time
from bs4 import BeautifulSoup

class Twayair:

    def __init__(self):

        #必要请求参数(用send_parameter方法请求获得)
        self.session = ""
        self._csrf = ""
        self.bt = ""
        
        #代理ip
        self.proxy = {}

        #出发到达日期(send_parameter方法里使用)
        self.go = "CJU"
        self.to = "GMP"
        self.date = "2019-11-11"

        #记录中间页请求成功与否
        self.send_parameter_status = False

        #回来数据的页面
        self.data_all = ""

        #获取代理IP
        self.get_proxy()
        #拿请求参数
        self.get_parameter()
        #发送请求参数
        self.send_parameter()
        #拿数据
        self.get_data()

    def get_proxy(self):
        #-----------------------------------------------------------------
        #请求报文
        url = "http://139.224.252.126:8066/api/ProxyIP/getip"
        parameter = {
            "GetNew":"1"
            ,"Operator":"100026"
            ,"InvalidAirlinesID":"616"
            ,"extractCount":"1"
            ,"protocolType":"11"
        }
        #-----------------------------------------------------------------
        #发送请求
        r = requests.get(url=url,params=parameter)
        r_text = r.text #响应内容
        r_text_len = len(r_text) #响应长度
        status_code = r.status_code #状态码
        #-----------------------------------------------------------------
        #处理请求
        if status_code != 200 and r_text =="\"[]\"":
            print("获取代理IP失败:",status_code)
        else:
            print("获取ip成功",status_code)
            print(r_text)
            print(r_text_len)

            re_ip = re.findall("\d+.\d+.\d+.\d+:\d+",r_text)[0]
            print(re_ip)
            self.proxy = {
                "http":"http://"+re_ip,
                "https":"https://"+re_ip,
            }
        #-----------------------------------------------------------------

    def get_parameter(self):
        '''请求主页'''
        #---------------------------------------------------------------
        #请求报文
        url = "https://www.twayair.com/app/main" 
        headers = {
            "Host": "www.twayair.com"
            ,"Connection": "keep-alive"
            ,"Cache-Control": "max-age=0"
            ,"Upgrade-Insecure-Requests": "1"
            ,"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                           "Chrome/77.0.3865.120 Safari/537.36 "
            ,"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3"
            ,"Sec-Fetch-Site": "cross-site"
            ,"Accept-Encoding": "gzip, deflate, br"
            ,"Accept-Language": "zh-CN,zh;q=0.9"
            ,"Cookie": "SETTINGS_REGION=CN; SETTINGS_LANGUAGE=zh-CN;"
        }
        #---------------------------------------------------------------
        #发送请求
        r = requests.get(url=url,headers=headers,proxies=self.proxy) 
        r_text = r.text #响应内容
        status_code = r.status_code #状态码
        r_text_len = len(r_text) #响应内容长度
        #----------------------------------------------------------------
        #判断请求
        if r.status_code != 200:
            print("请求主页失败:",status_code)
            print("主页响应长度",r_text_len)
            with open("index_error.html","w",encoding="utf8")as f:
                f.write(r_text)
        else:
            print("请求主页成功:",status_code)
            print("主页响应长度",r_text_len)
            #-----------------------------------------------------------------
            #提取session
            self.session = "SESSION"+re.findall("SESSION(.*?);",str(r.headers))[0]+";"
            #-----------------------------------------------------------------
            #提取csrf
            soup = BeautifulSoup(r_text,"html.parser")
            for link in soup.find_all('meta'):
                if link.get("name") == "_csrf":
                    self._csrf = link.get("content")
                    break
            #-----------------------------------------------------------------
            #提取bookingticket
            self.bt = re.findall("var _t =(.*?);",r_text)[0].replace(' ','').replace("'","")
            #-----------------------------------------------------------------
            #打印
            # print("session:",self.session)
            # print("_csrf:",self._csrf)
            # print("bt:",self.bt)
            #-----------------------------------------------------------------

    def send_parameter(self):
        '''请求中间页'''
        #-----------------------------------------------------------------
        #先判断主页的请求是否成功
        if not self.session:
            print("主页未请求成功,send_parameter不往下执行")
            return
        #-----------------------------------------------------------------
        #构造请求报文
        url = "https://www.twayair.com/app/booking/chooseItinerary"
        headers = {
        "Host": "www.twayair.com"
        ,"Connection": "keep-alive"
        ,"Origin": "https://www.twayair.com"
        ,"Cache-Control": "max-age=0"
        ,"Upgrade-Insecure-Requests": "1"
        ,"Content-Type": "application/x-www-form-urlencoded"
        ,"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36"
        ,"Sec-Fetch-Mode": "navigate"
        ,"Sec-Fetch-User": "?1"
        ,"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3"
        ,"Sec-Fetch-Site": "same-origin"
        ,"Referer": "https://www.twayair.com/app/main"
        ,"Accept-Encoding": "gzip, deflate, br"
        ,"Accept-Language": "zh-CN,zh;q=0.9"
        ,"Cookie": "_ga=GA1.2.1531734403.1571737546; _gid=GA1.2.375787299.1571737546; SETTINGS_REGION=CN; SETTINGS_LANGUAGE=zh-CN;"+self.session+"SETTINGS_CURRENCY=CNY; wcs_bt=s_12514e83073b:1571737564; __dbl__pv=9; dable_uid=45530640.1571737576840; __ZEHIC7962=1571734155;"
        }
        data = "bookingTicket=<bt>&tripType=OW&bookingType=HI&promoCodeDetails.promoCode=&validPromoCode=&availabilitySearches%5B0%5D.depAirport=<chufa>&availabilitySearches%5B0%5D.arrAirport=<daoda>&availabilitySearches%5B0%5D.flightDate=<riqi>&availabilitySearches%5B1%5D.depAirport=&availabilitySearches%5B1%5D.arrAirport=&availabilitySearches%5B1%5D.flightDate=&availabilitySearches%5B2%5D.depAirport=&availabilitySearches%5B2%5D.arrAirport=&availabilitySearches%5B2%5D.flightDate=&availabilitySearches%5B3%5D.depAirport=&availabilitySearches%5B3%5D.arrAirport=&availabilitySearches%5B3%5D.flightDate=&availabilitySearches%5B4%5D.depAirport=&availabilitySearches%5B4%5D.arrAirport=&availabilitySearches%5B4%5D.flightDate=&paxCountDetails%5B0%5D.paxCount=1&paxCountDetails%5B1%5D.paxCount=0&paxCountDetails%5B2%5D.paxCount=0&availabilitySearches%5B0%5D.depAirportName=&availabilitySearches%5B0%5D.arrAirportName=&availabilitySearches%5B1%5D.depAirportName=&availabilitySearches%5B1%5D.arrAirportName=&availabilitySearches%5B2%5D.depAirportName=&availabilitySearches%5B2%5D.arrAirportName=&availabilitySearches%5B3%5D.depAirportName=&availabilitySearches%5B3%5D.arrAirportName=&availabilitySearches%5B4%5D.depAirportName=&availabilitySearches%5B4%5D.arrAirportName=&_csrf=<csrf>&pax=1&pax=0&pax=0&deptAirportCode=<chufa>&arriAirportCode=<daoda>&schedule=<riqi>".replace("<bt>",self.bt).replace("<chufa>",self.go).replace("<daoda>",self.to).replace("<riqi>",self.date).replace("<csrf>",self._csrf)
        #-----------------------------------------------------------------
        #发送请求
        r = requests.post(url=url,headers=headers,data=data,proxies=self.proxy)
        r_text = r.text #响应内容
        r_text_len = len(r_text) #响应长度
        status_code = r.status_code #状态码
        
        #-----------------------------------------------------------------
        #判断响应状况
        if status_code != 200:
            print("中间页请求失败:",status_code)
            print("中间页响应体长度:",r_text_len)
            self.send_parameter_status = False
        else:
            print("中间页请求成功",status_code)
            print("中间页响应体长度:",r_text_len)
            self.send_parameter_status = True

    def get_data(self):
        '''拿数据'''
        #-----------------------------------------------------------------
        #判断中间请求是否成功
        if not self.send_parameter_status:
            print("中间页请求未成功,getdata不往下执行")
            return
        #-----------------------------------------------------------------
        #请求报文
        url="https://www.twayair.com/app/booking/layerAvailabilityList"
        headers = {
            "Host": "www.twayair.com"
            ,"Connection": "keep-alive"
            ,"Accept": "text/html, */*; q=0.01"
            ,"Origin": "https://www.twayair.com"
            ,"X-Requested-With": "XMLHttpRequest"
            ,"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36"
            ,"Sec-Fetch-Mode": "cors"
            ,"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"
            ,"Sec-Fetch-Site": "same-origin"
            ,"Referer": "https://www.twayair.com/app/booking/chooseItinerary"
            ,"Accept-Encoding": "gzip, deflate, br"
            ,"Accept-Language": "zh-CN,zh;q=0.9"
            ,"Cookie": "_ga=GA1.2.1531734403.1571737546; _gid=GA1.2.375787299.1571737546; SETTINGS_REGION=CN; SETTINGS_LANGUAGE=zh-CN;"+self.session+"SETTINGS_CURRENCY=CNY; __dbl__pv=9; dable_uid=45530640.1571737576840; __ZEHIC7962=1571734155; wcs_bt=s_12514e83073b:1571737647; _gat_gtag_UA_18196299_2=1; __ZEHIC6330=N; __zjc7702=4937759376; NetFunnel_ID="
        }
        data = "_csrf="+self._csrf
        #-----------------------------------------------------------------
        #发送请求
        r = requests.post(url=url,headers=headers,data=data,proxies=self.proxy)
        r_text = r.text #响应内容
        r_text_len = len(r_text) #响应长度
        status_code = r.status_code #状态码
        #-----------------------------------------------------------------
        #判断请求
        if status_code != 200:
            print("请求数据页失败:",status_code)
            print("请求数据页响应长度:",r_text_len)
        else:
            print("请求数据页成功:",status_code)
            print("请求数据页响应长度:",r_text_len)
            self.data_all = r_text
            #保存html到本地
            with open("data.html","w",encoding="utf8") as f:
                f.write(r_text)
        #-----------------------------------------------------------------



print("*"*30)
os.sys
Twayair()
print("*"*30)