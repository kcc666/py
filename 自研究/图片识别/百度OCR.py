#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: kcc time:2020/4/8

from aip import AipOcr

APP_ID = '19321800'
API_KEY = 'wk15MCS4Vzn7mL5CFcegLhrl'
SECRET_KEY = 'p7fRKr1MAZimZbq3NTgZCF6R90ym7a52'

client = AipOcr(APP_ID, API_KEY, SECRET_KEY)

def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()

image = get_file_content(r"C:\Users\46321\Desktop\demo2.png")
res = client.basicGeneral(image);
for i in res['words_result']:
    print(i["words"])
# print(get_file_content(r"C:\Users\46321\Desktop\demo.png"))