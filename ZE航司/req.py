#codding = utf8
import requests,json,os


def get_index():
    # 请求主页
    url = "https://www.eastarjet.com/newstar/PGWHC00001"
    headers = {
        "Host": "www.eastarjet.com"
        ,"Connection": "keep-alive"
        ,"Upgrade-Insecure-Requests": "1"
        ,"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36"
        ,"Sec-Fetch-Mode": "navigate"
        ,"Sec-Fetch-User": "?1"
        ,"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3"
        ,"Sec-Fetch-Site": "none"
        ,"Accept-Encoding": "gzip, deflate, br"
        ,"Accept-Language": "zh-CN,zh;q=0.9"
    }

    r = requests.get(url,headers=headers)
    print(r.status_code)
    print(r.headers)

def get_data(go,to,date):
    #请求数据
    url = "https://www.eastarjet.com/json/dataService"

    headers = {
        "Host": "www.eastarjet.com"
        ,"Connection": "keep-alive"
        ,"Origin": "https://www.eastarjet.com"
        ,"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36"
        ,"Content-type": "text/plain"
        ,"Accept": "*/*"
        ,"Sec-Fetch-Site": "same-origin"
        ,"Referer": "https://www.eastarjet.com/newstar/PGWHC00001"
        ,"Accept-Encoding": "gzip, deflate, br"
        ,"Accept-Language": "zh-CN,zh;q=0.9"
        ,"Cookie": "JSESSIONID=79C861E0D9F020571928762BE70FE608.WAS_93.WAS_93"
        ,"Content-Length": "1610"
    }

    cf = go
    dd = to
    date = date
    data = r'{"id": 11, "method": "DataService.service", "params": [{"javaClass": "com.jein.framework.connectivity.parameter.RequestParameter", "requestUniqueCode": "PGWHC00001", "requestExecuteType": "BIZ", "DBTransaction": false, "sourceName": null, "sourceExtension": null, "functionName": "DTWBA00022", "panelId": null, "methodType": null, "inParameters": {"javaClass": "java.util.List", "list": [{"javaClass": "com.jein.framework.connectivity.parameter.InParameter", "paramName": "flightSearch", "ioType": "IN", "structureType": "FIELD", "data": {"javaClass": "java.util.List", "list": [{"map": {"flightSearch": "{\"viewType\":\"B\",\"fly_type\":\"2\",\"person1\":\"1\",\"person2\":\"0\",\"person3\":\"0\",\"residentCountry\":\"KR\",\"currency\":\"\",\"promotion_cd\":\"\",\"flySection\":[{\"departure_cd\":\"ICN\",\"departure_txt\":\"\",\"arrival_cd\":\"TPE\",\"arrival_txt\":\"\",\"departure_date_cd\":\"20191002\",\"departure_date_txt\":\"\"}],\"recaptchaToken\":\"03AOLTBLR0-StEIwDrFmDfMK0JXuxTfkf2Gca4rLjvwEM7bPFoCfI4QeU1MDPSDik7UAvEZOadnzzkcZc1NmDo-ZoEy_VX46Y5iebUE05GQJzsGIH-HZHbtrnvMqjNjUI-7k19Ojn5n5LcqplZT8R4-5Ys08o7I5fwRA0ri9Tg7ACVFRnb-U1QDaNDYaCuZW8oDwxt1RptMaiEplaPHUdFybsW_km-9ksugcNZcE694-0yfS8Muuig1ivpsodqBu-44mbQesiNGxLmuKujo8GP5nO4OzA5z5AmVpEY_q4BVsP767VAvhfb0vkEue2C7PpVRuCyncxLo01Rlu7oxPe_YUlWWXyCLhYn2_c6PXcIipB-PwUQnmLX1qRLzekvK5H-2B39m91f1YSKNciU4octoKNIXk7-ZLKpJGtlm0jXTjYe5GSJ2DFIWL0QWhnAXHr5uZtXpqVzcFyRjeXCRpqxgFVc8I-qkOxuyA\"}"}, "javaClass": "java.util.Map"}]}}]}, "filterParameter": {"javaClass": "java.util.Map", "map": {}}}]}'.replace("ICN",cf).replace("TPE",dd).replace("20191002",date)
    r = requests.post(url,headers=headers,data=data,verify=False)
    # print(r.status_code)
    r_text = r.text
    if (len(r_text) < 1000):
        print("没有数据")
        print(r.text)
    else:
        os.system("cls")
        dct_text = json.loads(r_text)
        list_trips = dct_text["result"][0]["resultData"][0]["FlightSearch"]["trips"][0]

        #航班信息条数
        list_len = len(list_trips)
        print("获取航班信息{}条".format(list_len))

        for item in list_trips:
            #航班号
            fly_number = item["flightNumberText"]
            #出发时间
            fly_dep_date = item["standardTimeOfDeparture"]
            #到达时间
            fly_arr_date = item["standardTimeOfArrival"]
            #正常票价
            fly_zc = item["y_amount"]
            #折扣票价
            fly_zk = item["d_amount"]
            #特价票价
            if "e_amount" not in item:
                fly_tj = "已售空"
            else:
                fly_tj = item["e_amount"]
            
            print("航班号:",fly_number)
            print("出发时间:",fly_dep_date)
            print("到达时间:",fly_arr_date)
            print("正常票价:",fly_zc)
            print("折扣票价:",fly_zk)
            print("特价票价:",fly_tj)
            print("*"*30)


# get_index()
print("请等待")
get_data("ICN","NRT","20191016")
print("抓取完毕")
# def get_info():
#     go_city = input("请输入出发地机场码\n")
#     to_city = input("请输入到达地机场码\n")
#     go_date = input("请输入出发日期\n")
# get_data("HKG","ICN","20191031")

