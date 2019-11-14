import requests,json,os,re,time
from bs4 import BeautifulSoup
from lxml import etree

class Tw_order:
    def __init__(self,go,to,date):

        #必要请求参数(用send_parameter方法请求获得)
        self.session = ""
        self._csrf = ""
        self.bt = ""
        
        #代理ip
        self.proxy = {}

        #出发到达日期(send_parameter方法里使用)
        self.go = go
        self.to = to
        self.date = date

        #记录中间页请求成功与否
        self.send_parameter_status = False
        #记录登录页请求成功与否
        self.login_status = False
        #记录行李绑定请求成功与否
        self.bundle_status = False
        #回来数据的页面
        self.data_all = ""

        self.main()

    def main(self):
        #获取代理IP
        self.get_proxy()
        #拿请求参数
        self.get_parameter()

        #登录
        self.login()
        
        self.bundle()
        #发送请求参数
        # self.send_parameter()
        #拿数据
        # self.get_data()
        
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
        if status_code != 200 or r_text_len <=10:
            print("获取代理IP失败,不使用代理")
            # print(r_text)
        else:
            print("获取ip成功",status_code)
            # print(r_text)
            # print(r_text_len)

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
        try:
            r = requests.get(url=url,headers=headers,proxies=self.proxy) 
        except BaseException as e:
            print(e)
            print("请求主页时异常,可能是代理错误.")
            return
        r_text = r.text #响应内容
        status_code = r.status_code #状态码
        r_text_len = len(r_text) #响应内容长度
        #----------------------------------------------------------------
        #判断请求
        if r.status_code != 200:
            print("请求主页失败:",status_code)
            print("主页响应长度",r_text_len)
            print("主页内容:",r_text)
            with open("index_error.html","w",encoding="utf8")as f:
                f.write(r_text)
        else:
            print("请求主页成功:",status_code)
            print("主页响应长度",r_text_len)
            #-----------------------------------------------------------------
            #提取session
            try:
                self.session = "SESSION"+re.findall("SESSION(.*?);",str(r.headers))[0]+";"
            except:
                print("session提取失败")
                return
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
        try:
            r = requests.post(url=url,headers=headers,data=data,proxies=self.proxy)
        except BaseException as e:
            print("请求中间页异常,可能是代理错误")
            return
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

    def login(self):
        '''登录请求'''
        #-----------------------------------------------------------------
        #先判断主页的请求是否成功
        if not self.session:
            print("主页未请求成功,send_parameter不往下执行")
            return
        #-----------------------------------------------------------------
        #构造请求报文
        url = "https://www.twayair.com/app/login/memberLoginExec"
        headers = {
            "Host": "www.twayair.com"
            ,"Connection": "keep-alive"
            ,"Cache-Control": "max-age=0"
            ,"Origin": "https://www.twayair.com"
            ,"Upgrade-Insecure-Requests": "1"
            ,"Content-Type": "application/x-www-form-urlencoded"
            ,"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36"
            ,"Sec-Fetch-User": "?1"
            ,"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3"
            ,"Sec-Fetch-Site": "same-origin"
            ,"Sec-Fetch-Mode": "navigate"
            ,"Referer": "https://www.twayair.com/app/login/memberLogin"
            ,"Accept-Encoding": "gzip, deflate, br"
            ,"Accept-Language": "zh-CN,zh;q=0.9"
            ,"Cookie": "SETTINGS_REGION=CN; SETTINGS_LANGUAGE=zh-CN; _ga=GA1.2.41645099.1573556116; _gid=GA1.2.2097103302.1573556116; SETTINGS_CURRENCY=CNY; _fbp=fb.1.1573556122492.1237552267; dable_uid=48675685.1573556124606; __lt__cid=0a0b05c9-ac5a-4abc-9f8f-e74e531339d8; NetFunnel_ID=; "+self.session+"; __dbl__pv=1; __lt__sid=e97ea1e9-95565657; __z_a=2576909561190316533119031; __ZEHIC7131=1573608886; __ZEHIC987=1573609124; __zjc4915=4943638863; _gat_gtag_UA_18196299_2=1; wcs_bt=s_12514e83073b:1573610178"

        }
        data = "loginId=Aa960319&loginPassword=himyidea123&saveIdChk=N&autoLoginChk=N&socialCertDiv=&socialCertInfo=&returnUrl=&returnParameterNames=&returnParameterValues=&returnSubmitType=&"+"_csrf="+self._csrf
        #-----------------------------------------------------------------
        #发送请求
        try:
            r = requests.post(url=url,headers=headers,data=data,proxies=self.proxy)
        except BaseException as e:
            print("请求中间页异常,可能是代理错误")
            return

        r_text = r.text #响应内容
        r_text_len = len(r_text) #响应长度
        status_code = r.status_code #状态码
        
        #-----------------------------------------------------------------
        #判断响应状况
        if status_code != 200:
            with open("login_error.html","w",encoding="utf8")as f:
                f.write(r_text)
            print("登录请求失败:",status_code)
            print("登录请求页长度:",r_text_len)
            self.login_status = False
        else:
            print("登录请求成功",status_code)
            print("登录请求页长度:",r_text_len)
            self.login_status = True

    def bundle(self):
        '''行李绑定请求'''
        #-----------------------------------------------------------------
        #先判断主页的请求是否成功
        if not self.login_status:
            print("登录请求失败,bundle不往下执行")
            return
        #-----------------------------------------------------------------
        #构造请求报文
        url = "https://www.twayair.com/app/booking/bundle"
        headers = {
            "Host": "www.twayair.com"
            ,"Connection": "keep-alive"
            ,"Cache-Control": "max-age=0"
            ,"Origin": "https://www.twayair.com"
            ,"Upgrade-Insecure-Requests": "1"
            ,"Content-Type": "application/x-www-form-urlencoded"
            ,"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36"
            ,"Sec-Fetch-User": "?1"
            ,"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3"
            ,"Sec-Fetch-Site": "same-origin"
            ,"Sec-Fetch-Mode": "navigate"
            ,"Referer": "https://www.twayair.com/app/booking/chooseItinerary"
            ,"Accept-Encoding": "gzip, deflate, br"
            ,"Accept-Language": "zh-CN,zh;q=0.9"
            ,"Cookie": "SETTINGS_REGION=CN; SETTINGS_LANGUAGE=zh-CN; _ga=GA1.2.41645099.1573556116; _gid=GA1.2.2097103302.1573556116; SETTINGS_CURRENCY=CNY; _fbp=fb.1.1573556122492.1237552267; dable_uid=48675685.1573556124606; __lt__cid=0a0b05c9-ac5a-4abc-9f8f-e74e531339d8; "+self.session+" __lt__sid=e97ea1e9-95565657; __z_a=2576909561190316533119031; __ZEHIC7131=1573608886; __ZEHIC987=1573609124; __zjc6282=4943644826; __dbl__pv=2; wcs_bt=s_12514e83073b:1573611393; NetFunnel_ID="
        }
        data = {
            "_csrf":self._csrf
            ,"arriAirportCode":"ICN"
            ,"availabilitySearches[0].arrAirport":"ICN"
            ,"availabilitySearches[0].arrAirportName":"首尔/仁川"
            ,"availabilitySearches[0].depAirport":"NRT"
            ,"availabilitySearches[0].depAirportName":"东京/成田"
            ,"availabilitySearches[0].flightDate":"2019-11-21"
            ,"availabilitySearches[1].arrAirport":""
            ,"availabilitySearches[1].depAirport":""
            ,"availabilitySearches[1].flightDate":""
            ,"availabilitySearches[2].arrAirport":""
            ,"availabilitySearches[2].depAirport":""
            ,"availabilitySearches[2].flightDate":""
            ,"availabilitySearches[3].arrAirport":""
            ,"availabilitySearches[3].depAirport":""
            ,"availabilitySearches[3].flightDate":""
            ,"bookingTicket":self.bt
            ,"bookingType":"HI"
            ,"deptAirportCode":"NRT"
            ,"FareInfoForGuestType":"SegmentId=1&FlightSegmentGroupId=1&FareType=EventFare&FareLevel=EW&FareBasisCode=BYI&FareClass=B&PaxType=ADULT&FareTransactionId=336987&BaseFare=5000.0&Currency=JPY"
            ,"FlightSegmentInfo":"SegmentId=1&CarrierCode=TW&FltNumber=214&FlightDate=2019-11-21&FlightDateWithDay=2019-11-21(星期四)&FareClass=B&JourneyTime=0&FlightSegmentGroupId=1&JourneyTime=02:50&ArrivalDayChange=0&AircraftType=737&AircraftVersion=800&Stops=0&DepartureTime=19:00&ArrivalTime=21:50&DepAirport=NRT&DepartureTimeZone=GMT+09:00&ScheduledDepartureDateTimeLTC=2019-11-21T19:00:00&ScheduledDepartureDateTimeUTC=2019-11-21T10:00:00&ArrAirport=ICN&ArrivalTimeZone=GMT+09:00&ScheduledArrivalDateTimeLTC=2019-11-21T21:50:00&ScheduledArrivalDateTimeUTC=2019-11-21T12:50:00"
            ,"pax":"0"
            ,"pax":"1"
            ,"pax":"0"
            ,"PaxCountDetails":"PaxType=ADULT&PaxCount=1"
            ,"paxCountDetails[0].paxCount":"1"
            ,"paxCountDetails[1].paxCount":"0"
            ,"paxCountDetails[2].paxCount":"0"
            ,"promoCodeDetails.promoCode":""
            ,"routeCount":"1"
            ,"schedule":"2019-11-21"
            ,"tripType":"OW"
            ,"validPromoCode":""
        }
        
        #-----------------------------------------------------------------
        #发送请求
        try:
            r = requests.post(url=url,headers=headers,data=data,proxies=self.proxy)
        except BaseException as e:
            print("bundle请求异常")
            print(e)
            return

        r_text = r.text #响应内容
        r_text_len = len(r_text) #响应长度
        status_code = r.status_code #状态码
        
        #-----------------------------------------------------------------
        #判断响应状况
        if status_code != 200:
            with open("bundle_error.html","w",encoding="utf8")as f:
                f.write(r_text)
            print("行李绑定请求失败:",status_code)
            print("行李绑定请求页长度:",r_text_len)
            self.bundle_status = False
        else:
            with open("bundle_success.html","w",encoding="utf8")as f:
                f.write(r_text)
            print("行李绑定请求成功",status_code)
            print("行李绑定请求页长度:",r_text_len)
            self.bundle_status = True

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
        try:
            r = requests.post(url=url,headers=headers,data=data,proxies=self.proxy)
        except:
            print("请求数据页抛异常,可能是代理错误")
            return
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

    

if __name__ == "__main__":  
    
    os.system("cls")
    print("*"*30)
    Tw_order("NRT","ICN","2019-11-21")
    print("*"*30)