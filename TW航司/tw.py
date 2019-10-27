import requests,json,os,re,time
from bs4 import BeautifulSoup
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)



#请求JS_ID
def get_index():
    
    url = "https://www.twayair.com/app/main"

    headers = {
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

    proxy = {
        "http": "http://117.70.38.175:4227",
        "https":"https://117.70.38.175:4227",
    }
    

    r = requests.get(url=url,headers=headers,verify=False,timeout=30)

    if r.status_code != 200:
        print("请求主页失败")
        print(r.content.decode("utf8"))
        return
    else:
        print("主页请求状态码:",r.status_code)

    try:
        session = "SESSION"+re.findall("SESSION(.*?);",str(r.headers))[0]
        with open("Session.txt","w",encoding="utf8")as f:
            f.write(session)
        
        with open("body.html","w",encoding="utf8")as f:
            f.write(r.text)
    except:
        print("拿不到session")
        print(r.headers)

#取_csrl和bookingticket和SESSION和__z_a
def get_parameter():

    #返回的参数
    parameter = {
        "_csrf":"",
        "bookingticket":"",
        "SESSION":""
    }
    
    #session
    with open("Session.txt","r")as f:
        parameter["SESSION"] = f.read()+";"
    
    #_csrf
    with open("body.html","rb",)as f:
        text = f.read().decode("utf8")
        soup = BeautifulSoup(text,"html.parser")
        
        for link in soup.find_all('meta'):
            if link.get("name") == "_csrf":
                parameter["_csrf"] = link.get("content")

    #bookingticket
    bt = re.findall("var _t =(.*?);",text)[0].replace(' ','').replace("'","")
    parameter["bookingticket"] = bt

    return parameter
    
#第一次请求,填参数我的
def get_data1(go,to,date):

    parameter = get_parameter()
    session = parameter["SESSION"]
    csrf = parameter["_csrf"] #csrf参数
    bt = parameter["bookingticket"] #bt参数

    #爬数
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
        ,"Cookie": "_ga=GA1.2.1531734403.1571737546; _gid=GA1.2.375787299.1571737546; SETTINGS_REGION=CN; SETTINGS_LANGUAGE=zh-CN;"+session+"SETTINGS_CURRENCY=CNY; wcs_bt=s_12514e83073b:1571737564; __dbl__pv=9; dable_uid=45530640.1571737576840; __ZEHIC7962=1571734155;"
    }

    data = "bookingTicket=<bt>&tripType=OW&bookingType=HI&promoCodeDetails.promoCode=&validPromoCode=&availabilitySearches%5B0%5D.depAirport=<chufa>&availabilitySearches%5B0%5D.arrAirport=<daoda>&availabilitySearches%5B0%5D.flightDate=<riqi>&availabilitySearches%5B1%5D.depAirport=&availabilitySearches%5B1%5D.arrAirport=&availabilitySearches%5B1%5D.flightDate=&availabilitySearches%5B2%5D.depAirport=&availabilitySearches%5B2%5D.arrAirport=&availabilitySearches%5B2%5D.flightDate=&availabilitySearches%5B3%5D.depAirport=&availabilitySearches%5B3%5D.arrAirport=&availabilitySearches%5B3%5D.flightDate=&availabilitySearches%5B4%5D.depAirport=&availabilitySearches%5B4%5D.arrAirport=&availabilitySearches%5B4%5D.flightDate=&paxCountDetails%5B0%5D.paxCount=1&paxCountDetails%5B1%5D.paxCount=0&paxCountDetails%5B2%5D.paxCount=0&availabilitySearches%5B0%5D.depAirportName=&availabilitySearches%5B0%5D.arrAirportName=&availabilitySearches%5B1%5D.depAirportName=&availabilitySearches%5B1%5D.arrAirportName=&availabilitySearches%5B2%5D.depAirportName=&availabilitySearches%5B2%5D.arrAirportName=&availabilitySearches%5B3%5D.depAirportName=&availabilitySearches%5B3%5D.arrAirportName=&availabilitySearches%5B4%5D.depAirportName=&availabilitySearches%5B4%5D.arrAirportName=&_csrf=<csrf>&pax=1&pax=0&pax=0&deptAirportCode=<chufa>&arriAirportCode=<daoda>&schedule=<riqi>".replace("<bt>",bt).replace("<chufa>",go).replace("<daoda>",to).replace("<riqi>",date).replace("<csrf>",csrf)

    r = requests.post(url,headers=headers,data=data)
    print("请求参数状态码:",r.status_code)

#第二次请求,拿数据
def get_data2():
    url = "https://www.twayair.com/app/booking/layerAvailabilityList"

    parameter = get_parameter()
    session = parameter["SESSION"]
    csrf = parameter["_csrf"] #csrf参数

    data = "_csrf="+csrf

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
        ,"Cookie": "_ga=GA1.2.1531734403.1571737546; _gid=GA1.2.375787299.1571737546; SETTINGS_REGION=CN; SETTINGS_LANGUAGE=zh-CN;"+session+"SETTINGS_CURRENCY=CNY; __dbl__pv=9; dable_uid=45530640.1571737576840; __ZEHIC7962=1571734155; wcs_bt=s_12514e83073b:1571737647; _gat_gtag_UA_18196299_2=1; __ZEHIC6330=N; __zjc7702=4937759376; NetFunnel_ID="
    }
    r = requests.post(url,headers=headers,data=data)
    print("请求数据状态码",r.status_code)
    with open("data.html","w",encoding="utf8") as f:
        f.write(r.text)


#主函数
def main():
    # req_key()
    #从本地提取已保存的参数
    # za = get_key()
    #拿着参数去请求主页
    get_index()
    #第一次请求
    get_data1("CJU","GMP","2019-11-08")
    #第二次请求
    get_data2()


if __name__ == "__main__":
    main()
