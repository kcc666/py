import requests,json,os,re,time
from bs4 import BeautifulSoup
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)





class Tw:

    def __init__(self,chufa,daoda,date,proxy):

        #公共会话
        self.s = requests.Session()
        
        #出发参数
        self.chufa = chufa
        self.daoda = daoda
        self.date = date

        if proxy == "1":
            self.proxy = {}
        else:
            self.proxy ={
                "http": "http://"+proxy,
                "https":"https://"+proxy,
            }

        #主页url和headers
        self.index_url = "https://www.twayair.com/app/main"
        self.index_headers = {
            "Host": "www.twayair.com"
            ,"Connection": "keep-alive"
            ,"Cache-Control": "max-age=0"
            ,"Upgrade-Insecure-Requests": "1"
            ,"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36"
            ,"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3"
            ,"Sec-Fetch-Site": "cross-site"
            ,"Accept-Encoding": "gzip, deflate, br"
            ,"Accept-Language": "zh-CN,zh;q=0.9"
            ,"Cookie": "SETTINGS_REGION=CN; SETTINGS_LANGUAGE=zh-CN;"
        }

        #发送请求参数url和headers
        self.send_parameter_url="https://www.twayair.com/app/booking/chooseItinerary"
        self.send_parameter_headers = {
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
        }

        #拿数据请求url和headers
        self.get_data_url = "https://www.twayair.com/app/booking/layerAvailabilityList"
        self.get_data_headers = {
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
        }


        #拿主页text
        self.index_text = self.get_index()
        #解析主页拿参数
        self.parameter = self.get_parameter(self.index_text)
        #用拿到的参数请求中间页
        self.send_parameter_status = self.send_parameter(self.parameter)
        #请求最终数据
        self.data = self.get_data()




    #请求主页
    def get_index(self):
        try:
            r = self.s.get(url=self.index_url,headers=self.index_headers,proxies=self.proxy,verify=False)
            if r.status_code == 200:
                print("get_index:200")
                with open("index.html","w",encoding="utf8")as f:
                    f.write(r.content.decode("utf8"))
                    return r.content.decode("utf8")
            else:
                print("get_index:",r.status_code)
                print("get_index:",r.text)
                return "error"
        except Exception as e:
            print(e)
            print("get_index:请求主页抛异常")
            return "error"

    #提取参数
    def get_parameter(self,text):

        if text == "error":
            return "error"
        
        parameter = {
            "_csrf":"",
            "bookingticket":"",
        }
        
        #_csrf
        soup = BeautifulSoup(text,"html.parser")
        for link in soup.find_all('meta'):
            if link.get("name") == "_csrf":
                parameter["_csrf"] = link.get("content")
                break

        #bookingticket
        bt = re.findall("var _t =(.*?);",text)[0].replace(' ','').replace("'","")
        parameter["bookingticket"] = bt
        
        print("get_parameter:",parameter)
        return parameter

    #请求中间页
    def send_parameter(self,para):


        if para == "error":
            return "error"
        
        #准备数据
        csrf = para["_csrf"]
        bt = para["bookingticket"]
        data = "bookingTicket=<bt>&tripType=OW&bookingType=HI&promoCodeDetails.promoCode=&validPromoCode=&availabilitySearches%5B0%5D.depAirport=<chufa>&availabilitySearches%5B0%5D.arrAirport=<daoda>&availabilitySearches%5B0%5D.flightDate=<riqi>&availabilitySearches%5B1%5D.depAirport=&availabilitySearches%5B1%5D.arrAirport=&availabilitySearches%5B1%5D.flightDate=&availabilitySearches%5B2%5D.depAirport=&availabilitySearches%5B2%5D.arrAirport=&availabilitySearches%5B2%5D.flightDate=&availabilitySearches%5B3%5D.depAirport=&availabilitySearches%5B3%5D.arrAirport=&availabilitySearches%5B3%5D.flightDate=&availabilitySearches%5B4%5D.depAirport=&availabilitySearches%5B4%5D.arrAirport=&availabilitySearches%5B4%5D.flightDate=&paxCountDetails%5B0%5D.paxCount=1&paxCountDetails%5B1%5D.paxCount=0&paxCountDetails%5B2%5D.paxCount=0&availabilitySearches%5B0%5D.depAirportName=&availabilitySearches%5B0%5D.arrAirportName=&availabilitySearches%5B1%5D.depAirportName=&availabilitySearches%5B1%5D.arrAirportName=&availabilitySearches%5B2%5D.depAirportName=&availabilitySearches%5B2%5D.arrAirportName=&availabilitySearches%5B3%5D.depAirportName=&availabilitySearches%5B3%5D.arrAirportName=&availabilitySearches%5B4%5D.depAirportName=&availabilitySearches%5B4%5D.arrAirportName=&_csrf=<csrf>&pax=1&pax=0&pax=0&deptAirportCode=<chufa>&arriAirportCode=<daoda>&schedule=<riqi>".replace("<bt>",bt).replace("<chufa>",self.chufa).replace("<daoda>",self.daoda).replace("<riqi>",self.date).replace("<csrf>",csrf)

        try:
            #发送请求
            r = self.s.post(url=self.send_parameter_url,headers=self.send_parameter_headers,data=data,proxies=self.proxy,verify=False)
            if r.status_code == 200:
                print(len(r.text))
                print("send_parameter:中间页请求成功")
                return "success"
            else:
                print("send_parameter:失败,状态码:",r.status_code)
                return "error"
        except:
            print("send_parameter抛异常")
            return "error"

    #请求数据
    def get_data(self):
        if self.send_parameter_status == "error":
            return "error"

        try:
            data = "_csrf="+self.parameter["_csrf"]
            r = self.s.post(url=self.get_data_url,headers=self.get_data_headers,data=data,proxies=self.proxy,verify=False)
            if r.status_code == 200:
                # print(r.request.headers)
                print("get_data:请求成功",len(r.text))

                with open("data.html","w",encoding="utf8")as f:
                    res_text = r.content.decode("utf8")
                    f.write(res_text)
                    return res_text
            else:
                print("get_data:请求失败:",r.status_code)
                return "error"

        except:
            print("get_data:请求数据抛异常")
            return "error"


print("*"*30)
Tw("CJU","GMP","2019-11-08","106.5.253.245:4221")
print("*"*30)

#117.70.38.175:4227
#58.245.205.142:8090

# print(f'面向对象')
# carOne = Car('passat',250000)
# carOne.printCarInfo()
# carOne.driveDistance(100)
# carOne.driveDistance(200)
# print(f'passat已经行驶了{carOne.distance}公里')
# print(f'passat的价格是{carOne.price}')