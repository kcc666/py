import os
import requests
import json
import re
import lxml

#登录账号获得psid
def login():
    #请求头
    headers = {
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3732.400 QQBrowser/10.5.3819.400"
    }
    #携带参数
    d = {
        "username":"",
        "password":"",
        "remember":"true"
    }
    #请求地址
    url = "http://api.vps.321194.com/vps_new/users/login_do.html"


    try:
        #发送请求
        r = requests.post(url,headers = headers,data=d)
        #获取响应信息
        ret = json.loads(r.content.decode("utf8"))
        msg = ret["msg"]
        # print(msg)

        #获取PHPSESSID
        dct = dict(r.headers)["Set-Cookie"].split(";")[0]
        # print(dct)

        #返回值PHPSESSID
        print("登录成功")
        return dct
    except:
        print("登录失败")
        return "f"

#提取列表
def get_list(psid):
    if psid == "f":return "f"
    #请求头
    headers = {
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3732.400 QQBrowser/10.5.3819.400"
        ,"Cookie":psid
    }
    #携带参数
    d = {
        "page":"1",
        "type":"1"
    }
    #请求地址
    url = "http://api.vps.321194.com/vps_new/ucenter/server_list.html"
    try:
        #发送请求
        r = requests.get(url,headers = headers,params=d)
        #得到结果
        result = r.content.decode("utf8")
        print("获得页面列表",d["page"])
        return result
    except BaseException as e:
        print("请求失败:",e)
        return("f")

#解析字符串
def extract_data(text):
    if text == "f": return
    try:
        #去反斜杠
        n_t = text.replace("\\","")
        #提取标签
        t = re.findall('data-orderid .+?>',n_t)
        #去重
        n_list = []
        for a in t:
            if a not in n_list:
                n_list.append(a)
        #组成字典
        dct = []
        for i in n_list:
            r_item = re.findall('"(.*?)"',i)
            dct.append(r_item)
            print(r_item)
        return dct
    except BaseException as e:
        print("解析字符串失败")
        print(e)
        return

#提取过期时间
def get_date(psid):
    #请求头
    headers = {
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3732.400 QQBrowser/10.5.3819.400"
        ,"Cookie":psid
    }
    #携带参数
    d = {
        "id":"15165",
        "type":"1",
    }
    #请求地址
    url = "http://api.vps.321194.com/vps_new/ucenter/more_info.html"


    #发送请求
    r = requests.get(url,headers = headers,params=d)
    #获取响应信息
    ret = r.content.decode("utf8")
    # result = re.findall(,ret)
    # print(ret)
    ret = re.findall(r"(\d{4}-\d{1,2}-\d{1,2} \d{1,2}:\d{1,2}:\d{1,2})",ret)
    print(ret)

def main():
    os.system("cls")

    #拿到登录后的ID
    pid = login()
    #用ID爬取页面.得到页面字符串
    s_list_text = get_list(pid)
    #正则解析字符串
    dct = extract_data(s_list_text)
    #根据信息提取过期时间
    get_date(pid)

    
    
    


if __name__ == "__main__":
    main()