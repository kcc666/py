import requests
import time
from  bs4 import  BeautifulSoup
import execjs
from urllib import parse


class Splider():
    def __init__(self):
        self.session = requests.session()
        self.headers = {
    "href": "https://www.zhipin.com/"
    ,
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36",
}
        #初始为空
        self.token=''


    def tranform(self,string):
        dict_={}
        str=string.split('=')
        dict_[str[0]]=str[1]
        return dict_

    def parse_302(self,response):
        location_info = response.headers.get('location').split('&')
        name_info = location_info[1]
        url_info = location_info[0]
        name_info = self.tranform(name_info)
        name = name_info['name']

        seed_info = url_info.split('?')[1]
        seed_info = self.tranform(seed_info)
        seed = seed_info['seed']
        ts_info = location_info[2]
        ts_info = self.tranform(ts_info)
        ts = int(ts_info['ts'])
        print(seed,ts)
        js_res = requests.get("https://www.zhipin.com/web/common/security-js/" + name + ".js")
        js = r"""var window ={
                           navigator:{
                               userAgent:"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36",
                               webdriver:false
                               ,appVersion:"5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36",

                           }
                           ,screen:{
                               availHeight:824
                               ,availTop:0
                               ,height:864
                               ,availWidth:1920
                           }
                           ,document:{
                               getElementById:function(){}
                           }
                           ,moveBy:function(){}
                           ,open:function open() {}
                           ,moveTo:function(){}
                           ,outerWidth:1536,
                           innerWidth:0
                           ,outerHeight:824
                           ,innerHeight:0
                         }
                         var top ={
                           location:{
                               href:"https://www.zhipin.com/"
                           }
                         }

                         var document ={
                           getElementById:function(){return null}
                           ,title:""
                           ,createElement:function(){
                                var caption={tagName:"CAPTION"}
                                return caption
                               }
                         }
                         global =window
                        
                         function setInterval(){}
                         setInterval.toString = function(){return "function setInterval() { [native code] }"}
                       
                       
                         var process=undefined
                         var global=undefined
                         var child_process=undefined
                         var Buffer=undefined
                         var sessionStorage ='11';""" + js_res.text + r"""  function get(seed,ts){

                           code = new ABC().z(seed, parseInt(ts)+(480+new Date().getTimezoneOffset())*60*1000);
                           return code
                         }"""
        f_js = execjs.compile(js)
        print(parse.unquote(seed))
        self.token = f_js.call("get", parse.unquote(seed), ts)
        print(self.token)






    def Get(self,url):
            try:
                self.headers['cookie'] = "__zp_stoken__=" + parse.quote(self.token)
                res= self.session.get(url, headers=self.headers,allow_redirects=False)
                print(res.status_code)
                if res.status_code==200:
                   return res.text
                else:
                    self.parse_302(res)
                    return self.Get(url)

            except Exception as e:
                print(e)


    def parse_list(self,rep):
        soup = BeautifulSoup(rep, 'html.parser', from_encoding='utf-8')
        details_container = soup.select('.job-primary')
        for detail in details_container:
            company_infos={}
            job_name=detail.select('.job-name')[0].get_text()
            job_area=detail.select('.job-area-wrapper .job-area' )[0].get_text()
            red=detail.select('.red')[0].get_text()
            job_limit=detail.select('.job-limit p')[0].get_text()
            name=detail.select('.info-publis .name')[0].get_text()
            company_text=detail.select('.company-text')[0].get_text().replace('\n','')
            company_name=detail.select(".company-text .name")[0].get_text().replace('\n','')
            company_href=detail.select(".company-text a")[0].get('href')
            tag_tem=detail.select('.tag-item')[0].get_text().replace('\n','')
            info_desc=detail.select('.info-desc')[0].get_text().replace('\n','')
            company_logo=detail.select('.company-logo')[0].get('src')
            company_infos['职位'] = job_name
            company_infos['学历限制'] = job_limit
            company_infos['工资'] = red
            company_infos['地址'] = job_area
            company_infos['发布人'] = name
            company_infos['公司名称'] = company_name
            company_infos['公司网址'] = company_href
            company_infos['公司详情'] = company_text
            company_infos['公司标签'] = tag_tem
            company_infos['公司福利'] = info_desc
            company_infos['公司logo'] = company_logo
            yield company_infos


    def get_num(self,html):
        pass


    def  run(self):
        for i in range(1,10):
            url='https://www.zhipin.com/c100010000-p120201/?page={}'.format(i)
            html=self.Get(url)
            zhiweis=self.parse_list(html)
            for zhiwei in zhiweis:
                print(zhiwei)
            time.sleep(2)



if __name__ == '__main__':
    s=Splider()
    s.run()
