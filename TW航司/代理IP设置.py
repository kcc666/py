import requests
from bs4 import BeautifulSoup as bs
import re

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36"}
proxies = {
                "http": "http://58.245.205.142:8090",
                
            }

url='http://txt.go.sohu.com/ip/soip'#该网站会返回访问设备的公网ip地址

res = requests.get(url,headers=headers,proxies=proxies)

print(res.status_code)
html = res.text
ip = re.findall(r'\d+.\d+.\d+.\d+',html)#用正则表达式筛选出ip地址

print(ip)