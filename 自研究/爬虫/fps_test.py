import requests




def main():
    url = "https://wetest.qq.com/cube/Report?testid=ff2838c8e2b7463c08f71bd96170b365&mm=0fd2cb7c518a98e64118d563cee2ef69"
    headers = {
        "User-Agent":"PostmanRuntime/7.19.0",
        "Accept":"*/*",
        "Cache-Control":"no-cache",
        "Host":"wetest.qq.com",
        "Accept-Encoding":"gzip, deflate",
        "Connection":"keep-alive",
    }
    r = requests.Session()
    res1 = r.get(url=url,headers=headers)

    url1 = "ttps://wetest.qq.com/cube/Fps?testid=12177609&mm=0fd2cb7c518a98e64118d563cee2ef69"
    headers1 = {
        "Host": "wetest.qq.com"
        ,"Connection": "keep-alive"
        ,"Content-Length": "50"
        ,"Sec-Fetch-Mode": "cors"
        ,"Origin": "https://wetest.qq.com"
        ,"X-CSRF-TOKEN": "MXhlV053bFBjSgFiOUEmE0MpKC8sBlghZwENJnoYBjthCw0YNz0UFw=="
        ,"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36"
        ,"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"
        ,"Accept": "*/*"
        ,"X-Requested-With": "XMLHttpRequest"
        ,"Sec-Fetch-Site": "same-origin"
        ,"Referer": "https://wetest.qq.com/cube/Report?testid=ff2838c8e2b7463c08f71bd96170b365&mm=0fd2cb7c518a98e64118d563cee2ef69"
        ,"Accept-Encoding": "gzip, deflate, br"
        ,"Accept-Language": "zh-CN,zh;q=0.9"
    }
    data = {
        "testid": "12177609",
        "testType": "Performance_common_noroot"
    }

    res = r.post(url=url,headers=headers,data=data)
    print(res.status_code)

    with open("a.html","w",encoding="utf8")as f:
        f.write(res.text)
    print(res.status_code)


if __name__ == "__main__":
    main()