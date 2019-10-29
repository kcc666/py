import requests,json,os,re,time
from bs4 import BeautifulSoup
from lxml import etree

class Twayair:

    def __init__(self):

        #必要请求参数(用send_parameter方法请求获得)
        self.session = ""
        self._csrf = ""
        self.bt = ""
        
        #代理ip
        self.proxy = {}

        #出发到达日期(send_parameter方法里使用)
        self.go = "KOJ"
        self.to = "RMQ"
        self.date = "2019-11-09"

        #记录中间页请求成功与否
        self.send_parameter_status = False

        #回来数据的页面
        self.data_all = ""

        self.main()
        

    def main(self):
        #获取代理IP
        self.get_proxy()
        #拿请求参数
        self.get_parameter()
        #发送请求参数
        self.send_parameter()
        #拿数据
        self.get_data()
        #解析数据
        self.parse_data()

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

    def parse_data(self):
        '''解析数据'''
        if self.data_all == "":
            print("parse_data:没有可用解析数据,本方法不执行")
            return
        text1 = self.data_all

        data_all = [] #列表下的字典

        #将html文本解析为element对象
        html = etree.HTML(text1) #el对象

        #航班列表的 li
        airline_list = html.xpath("//div[@id='price_list_route_1']/ul/li")
        # print(len(airline_list))
        if len(airline_list) == 0:
            print("没有航班")
            return
        #遍历li
        for li_1 in airline_list:

            data_all_dict = {

                "dep_city":self.go #出发城市码
                ,"arr_city":self.to #到达城市码
                ,"dep_date":self.date #出发日期

                ,"air_tax1":"" #机建
                ,"air_tax2":"" #燃油(贵一些)
                ,"dep_time":"" #航班出发时间
                ,"arr_time":"" #航班到达时间
                ,"air_num":"" #航班号
                ,"hd_price":"售罄" #活动票价
                ,"zn_price":"" #智能票价
                ,"yb_price":"" #一般运费
            }

            #出发和到达时间
            air_dep_arr_times = li_1.xpath("./a/div/div[1]//strong/text()")

            #航班号
            air_numbers = li_1.xpath("./a/div/div[1]/button/text()")

            #赋值,出发时间到达时间航班号
            data_all_dict["air_num"] = air_numbers[0]
            data_all_dict["dep_time"] = air_dep_arr_times[0]
            data_all_dict["arr_time"] = air_dep_arr_times[1]

            #遍历每条航班下的活动,智能,一般票价的分别价格
            for item in li_1.xpath("./div/div"):
        
                #标题(活动,智能,或一般))
                label = item.xpath("./div[@class='select_rate']/label/text()[2]")[0]
                try:
                    #价格
                    price = item.xpath("./div[@class='rate_price']/strong/text()")[0]
                    #币种
                    currency = item.xpath("./div[@class='rate_price']/span[@class='unit']/text()")[0]
                    #机建
                    data_all_dict["air_tax1"] = item.xpath("./div[@class='select_rate']/div[last()]/@data-tax")[0]
                    #燃油
                    data_all_dict["air_tax2"] = item.xpath("./div[@class='select_rate']/div[last()]/@data-surcharge")[0]
                except:
                    price = "售罄"
                    currency = "无"
                    data_all_dict["air_tax1"] = "无"
                    data_all_dict["air_tax2"] = "无"
                
                

                if label =="活动票价":
                    data_all_dict["hd_price"] = price
                elif label =="智能票价":
                    data_all_dict["zn_price"] = price
                else:
                    data_all_dict["yb_price"] = price
            
            #把本条航班信息添加到数组&打印
            # print(data_all_dict)
            data_all.append(data_all_dict)
        
        #打印最后结果
        print(data_all)


os.system("cls")
print("*"*30)
Twayair()
print("*"*30)