# http://139.224.252.126:8066/api/ProxyIP/getip?GetNew=getNew&Operator=100026&InvalidAirlinesID=616&extractCount=1&protocolType=11

import requests,time,json,traceback
requests.packages.urllib3.disable_warnings()
from AirLccFareModel import AirRequest, AirLowFareRes, LowFare, DefaultConfig
from requests.exceptions import ReadTimeout, ProxyError, ConnectTimeout

class Twayair1():
    def __init__(self,paramRequest):
        # 判断传进来的实体是否是AirRequest类生成
        assert isinstance(paramRequest, AirRequest)

        # 定义响应实体
        self.response = AirLowFareRes()
        # 接收请求实体
        self.paramRequest = paramRequest
        # 定义会话
        self.session = requests.session()
        # 设置超时时间
        self.timeout = 20



    def main(self):
        #----------------------------------------------------------------------
        # 设置代理IP
        # try:
        #     ip = self.getVpsProxy()
        #     self.session.proxies = {
        #         "http": "http://"+ip,
        #         "https": "https://"+ip
        #     }
        # except Exception as e:
        #     print(traceback.format_exc(e))
        #----------------------------------------------------------------------
        # 获取数据
            try:
                self.searchFlight()
            except ProxyError:
                self.searchLowFareRes.ResultCode = 505
            except ConnectTimeout:
                self.searchLowFareRes.ResultCode = 507
            except ReadTimeout:
                self.searchLowFareRes.ResultCode = 507
            except Exception as e:
                self.searchLowFareRes.ResultCode = 500
                self.searchLowFareRes.Message = "searchError:"+str(e)[:50]


    def getVpsProxy(self):
        r = requests.get("http://139.224.252.126:8066/api/ProxyIP/getip?GetNew=getNew&Operator=100026&InvalidAirlinesID=616&extractCount=1&protocolType=11")
        ip = eval(json.loads(r.text))[0]
        return ip

    def searchFlight(self):
        '''拿数据'''
        # ----------------------------------------------------------------------
        # 第一个请求
        self.session.headers = {
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
        r1  = self.session.get("https://www.twayair.com/app/main",verify=False ,timeout=self.timeout)
        with open("index.html","wb")as f:
            f.write(r1.content)



if __name__ == '__main__':
    # 模拟一个请求实体a
    a = AirRequest()

    # 赋值请求实体
    a.DepAirport = "NRT"
    a.ArrAirport = "ICN"
    a.DepDate = "2019-12-20"
    a.AdultNum = 4
    a.ChildNum = 0

    s = Twayair1(a)

    # 调用Tw实体Main方法
    b = s.main()
    print(b)
