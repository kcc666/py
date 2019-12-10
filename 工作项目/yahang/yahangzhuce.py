#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: kcc time:2019/12/9

import requests
from selenium  import webdriver

r = requests.session()
r1 = r.get("https://www.airasiabig.com/cn/zh/registrationmobileios")

username = "masansan@yopmail.com"
password = "Aa888999"
FirstName = "DONGMEI"
LastName = "MA"
params =  "CustomerNumber=&Email=" + username + "&Password=" + password + "&FirstName=" + FirstName + "&LastName=" + LastName
r2 = r.post("https://www.airasiabig.com/cn/zh/registrationmobileios",params=params)
print(r2.status_code)