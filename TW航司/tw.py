import requests,json,os,re,time
from bs4 import BeautifulSoup
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


#IP防封的密钥za参数
def req_key():
    url = "https://www.twayair.com/__zenedge/f"

    headers = {
         "Host":"www.twayair.com"
        ,"Connection":"keep-alive"
        ,"Sec-Fetch-Mode":"cors"
        ,"Origin": "https//www.twayair.com"
        ,"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36"
        ,"Content-type":"application/json"
        ,"Accept": "*/*"
        ,"Sec-Fetch-Site":"same-origin"
        ,"Referer":"https://www.twayair.com/app/main"
        ,"Accept-Encoding":"gzip, deflate, br"
        ,"Accept-Language":"zh-CN,zh;q=0.9"
    }

    data = "data={\"UserAgent\":\"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36\",\"Language\":\"zh-CN\",\"ColorDepth\":24,\"PixelRatio\":1,\"HardwareConcurrency\":-1,\"ScreenResolution\":\"1920x1080\",\"AvailableScreenResolution\":\"1920x1040\",\"TimezoneOffset\":-480,\"SessionStorage\":true,\"LocalStorage\":true,\"IndexedDb\":true,\"DocumentBody\":false,\"OpenDatabase\":true,\"CpuClass\":\"unknown\",\"Platform\":\"Win32\",\"DoNotTrack\":\"unknown\",\"IsAdBlock\":false,\"LiedLanguages\":false,\"LiedResolution\":false,\"LiedOs\":false,\"LiedBrowser\":false,\"PluginsString\":\"Chrome PDF Plugin::Portable Document Format::application/x-google-chrome-pdf:pdf;Chrome PDF Viewer::::application/pdf:pdf;Native Client::::application/x-nacl:,application/x-pnacl:\",\"Fonts\":\"notselected\",\"CanvasFingerprint\":\"yes,26f0d4c5001a058236e4964f5b19c5578b83a158\",\"WebGl\":\"webgl fingerprint:bd6549c125f67b18985a8c509803f4b883ff810c;webgl extensions:ANGLE_instanced_arrays;EXT_blend_minmax;EXT_color_buffer_half_float;EXT_disjoint_timer_query;EXT_float_blend;EXT_frag_depth;EXT_shader_texture_lod;EXT_texture_filter_anisotropic;WEBKIT_EXT_texture_filter_anisotropic;EXT_sRGB;KHR_parallel_shader_compile;OES_element_index_uint;OES_standard_derivatives;OES_texture_float;OES_texture_float_linear;OES_texture_half_float;OES_texture_half_float_linear;OES_vertex_array_object;WEBGL_color_buffer_float;WEBGL_compressed_texture_s3tc;WEBKIT_WEBGL_compressed_texture_s3tc;WEBGL_compressed_texture_s3tc_srgb;WEBGL_debug_renderer_info;WEBGL_debug_shaders;WEBGL_depth_texture;WEBKIT_WEBGL_depth_texture;WEBGL_draw_buffers;WEBGL_lose_context;WEBKIT_WEBGL_lose_context;webgl status:[1, 1],[1, 1024],8,yes,8,24,8,16,32,16384,1024,16384,16,16384,30,16,16,4096,[32767, 32767],8,WebKit WebGL,WebGL GLSL ES 1.0 (OpenGL ES GLSL ES 1.0 Chromium),0,WebKit,WebGL 1.0 (OpenGL ES 2.0 Chromium),Google Inc.,ANGLE (Intel(R) UHD Graphics 620 Direct3D11 vs_5_0 ps_5_0),23,127,127,23,127,127,23,127,127,23,127,127,23,127,127,23,127,127,0,31,30,0,31,30,0,31,30,0,31,30,0,31,30,0,31,30\",\"TouchSupport\":\"0,false,false\",\"AudioContext\":\"ac-baseLatency:0.01, ac-sampleRate:48000, ac-state:suspended, ac-maxChannelCount:2, ac-numberOfInputs:1, ac-numberOfOutputs:0, ac-channelCount:2, ac-channelCountMode:explicit, ac-channelInterpretation:speakers, an-fftSize:2048, an-frequencyBinCount:1024, an-minDecibels:-100, an-maxDecibels:-30, an-smoothingTimeConstant:0.8, an-numberOfInputs:1, an-numberOfOutputs:1, an-channelCount:2, an-channelCountMode:max, an-channelInterpretation:speakers, \",\"DynamicCompressor\":\"24.8472016423475,301ef97ef03e6fa4e160380f7de8f8ed050a042e\"}"
    
    r = requests.post(url=url,headers=headers,data=data)

    print("get_key:",r.text)
    with open("za.txt","w",encoding="utf8")as f:
        f.write(r.text)

#取已保存的za参数
def get_key():
    with open("za.txt","r")as f:
        return "__z_a="+f.read()

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
    
#第一次请求,填参数
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
