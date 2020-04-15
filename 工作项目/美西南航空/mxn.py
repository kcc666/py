#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: kcc time:2020/4/9

import requests,json
requests.packages.urllib3.disable_warnings()
s = requests.session()

s.verify=False

s.headers = {
    "Host": "www.southwest.com",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
    "Sec-Fetch-Dest": "document",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-User": "?1",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9",
}
res_index_url = "https://www.southwest.com/"
res_index = s.get(url=res_index_url)

print(res_index.status_code)
print(len(res_index.text))

res_2_url = "https://www.southwest.com/api/air-booking/v1/air-booking/page/air/booking/shopping"
res_2_data = {"adultPassengersCount":"1","departureDate":"2020-04-20","departureTimeOfDay":"ALL_DAY","destinationAirportCode":"ALB","fareType":"USD","int":"HOMEQBOMAIR","originationAirportCode":"ABQ","passengerType":"ADULT","reset":"true","returnDate":"","returnTimeOfDay":"ALL_DAY","seniorPassengersCount":"0","tripType":"oneway","application":"air-booking","site":"southwest"}

res2 = s.post(url=res_2_url,data=json.dumps(res_2_data))
print(res2.status_code)
print(len(res2.text))