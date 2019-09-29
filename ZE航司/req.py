#codding = utf8
import requests


url = "https://www.eastarjet.com/json/dataService"

headers = {
    "Accept": "*/*"
    ,"Accept-Encoding": "gzip, deflate,br"
    ,"Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2"
    ,"Connection": "keep-alive"
    ,"Content-Length": "1584"
    ,"Content-type": "text/plain"
    ,"Cookie": "selected_country_code=CN; _ga=GA1.2.1638435572.1569560321; n$D=1; n$H=1; JSESSIONID=E448F9BED5DF1C564AD799D3282C2A5F.WAS_93.WAS_93; ROUTEID=route.WAS_93; selected_culture_code=zh_CN; _gid=GA1.2.1637321302.1569721939; n$cu=1569722002718; NetFunnel_ID=5002%3A200%3Akey%3D76EF2AAB8003E5C282A21E4D1524948B1541E09A7AFE382A814041630DE99262E631EEC891797F27F3954C75812329E49B621301EAA75FE94B0540B7A2569C4E3F4DF2BBB694A565DA78BC4475A9C404C2D11865947DBA25127EB672187D8E0FAB54CF4E571B7E11B71E389445A10A8063682C302C322C312C302C30%26nwait%3D0%26nnext%3D0%26tps%3D0%26ttl%3D0%26ip%3Dnetfunnel.eastarjet.com%26port%3D80"
    ,"Host":"www.eastarjet.com"
    ,"Referer": "https://www.eastarjet.com/newstar/PGWHC00001"
    ,"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:69.0) Gecko/20100101 Firefox/69.0"
}

data = {"JSON":{"id":"18","method":"DataService.service","params":[{"DBTransaction":"false","filterParameter":{"javaClass":"java.util.Map","map":"{}"},"functionName":"DTWBA00022","inParameters":{"javaClass":"java.util.List","list":[{"data":{"javaClass":"java.util.List","list":[{"javaClass":"java.util.Map","map":{"flightSearch":"{\"viewType\":\"B\",\"fly_type\":\"2\",\"person1\":\"1\",\"person2\":\"0\",\"person3\":\"0\",\"residentCountry\":\"KR\",\"currency\":\"\",\"promotion_cd\":\"\",\"flySection\":[{\"departure_cd\":\"CJU\",\"departure_txt\":\"济州\",\"arrival_cd\":\"PUS\",\"arrival_txt\":\"釜山\",\"departure_date_cd\":\"20190930\",\"departure_date_txt\":\"2019-09-30\"}],\"recaptchaToken\":\"03AOLTBLS0isxMvMFYTbBV-JjXdIb2xX4-kNSjwQ01MV-Scw2SDMPOhzNfPus89ClidVcMEYceHTmv7yvn7jzOh_CDraVyo97KSEfELilAAxWfHyCqb3JJr2MkcpEErzM-Pe4AGdLaJTp-B15JWQcaiqXBzdnjElO73EN3eqnanPVeUr9q160hQikHwkLYgS8l5s4NJCQWYPvu3autU-xiEFw4yh4ztc_s1O8stNIITh5nHmERxNKU9gKeyr6yNBE9pC_MsRiIA89PJNOue3F5efOl_v8G-LwxsKGmGwaBAqDDsa_Z2ntIe5ss7l24lqnJgcWCSBi8Lwkl8fNR8O-FyrgfkfjJqXAVBIm55LxbUGxxW7pPtJ8jP2hdqKIE3Ue3nJiD9vaGL_CLSTSdcqa1nyFTSBCy1kQlZMO_XwBb7GL5qyMm0stLCptrhMMCyWbjsQDv4XWytSA-u9QvYshHcI5a0LIS-3xf0Q\"}"}}]},"ioType":"IN","javaClass":"com.jein.framework.connectivity.parameter.InParameter","paramName":"flightSearch","structureType":"FIELD"}]},"javaClass":"com.jein.framework.connectivity.parameter.RequestParameter","methodType":"null","panelId":"null","requestExecuteType":"BIZ","requestUniqueCode":"PGWHC00001","sourceExtension":"null","sourceName":"null"}]},"请求载荷（payload）":{"EDITOR_CONFIG":{"text":"{\"id\": 18, \"method\": \"DataService.service\", \"params\": [{\"javaClass\": \"com.jein.framework.connectivity.parameter.RequestParameter\", \"requestUniqueCode\": \"PGWHC00001\", \"requestExecuteType\": \"BIZ\", \"DBTransaction\": false, \"sourceName\": null, \"sourceExtension\": null, \"functionName\": \"DTWBA00022\", \"panelId\": null, \"methodType\": null, \"inParameters\": {\"javaClass\": \"java.util.List\", \"list\": [{\"javaClass\": \"com.jein.framework.connectivity.parameter.InParameter\", \"paramName\": \"flightSearch\", \"ioType\": \"IN\", \"structureType\": \"FIELD\", \"data\": {\"javaClass\": \"java.util.List\", \"list\": [{\"map\": {\"flightSearch\": \"{\\\"viewType\\\":\\\"B\\\",\\\"fly_type\\\":\\\"2\\\",\\\"person1\\\":\\\"1\\\",\\\"person2\\\":\\\"0\\\",\\\"person3\\\":\\\"0\\\",\\\"residentCountry\\\":\\\"KR\\\",\\\"currency\\\":\\\"\\\",\\\"promotion_cd\\\":\\\"\\\",\\\"flySection\\\":[{\\\"departure_cd\\\":\\\"CJU\\\",\\\"departure_txt\\\":\\\"\\u6d4e\\u5dde\\\",\\\"arrival_cd\\\":\\\"PUS\\\",\\\"arrival_txt\\\":\\\"\\u91dc\\u5c71\\\",\\\"departure_date_cd\\\":\\\"20190930\\\",\\\"departure_date_txt\\\":\\\"2019-09-30\\\"}],\\\"recaptchaToken\\\":\\\"03AOLTBLS0isxMvMFYTbBV-JjXdIb2xX4-kNSjwQ01MV-Scw2SDMPOhzNfPus89ClidVcMEYceHTmv7yvn7jzOh_CDraVyo97KSEfELilAAxWfHyCqb3JJr2MkcpEErzM-Pe4AGdLaJTp-B15JWQcaiqXBzdnjElO73EN3eqnanPVeUr9q160hQikHwkLYgS8l5s4NJCQWYPvu3autU-xiEFw4yh4ztc_s1O8stNIITh5nHmERxNKU9gKeyr6yNBE9pC_MsRiIA89PJNOue3F5efOl_v8G-LwxsKGmGwaBAqDDsa_Z2ntIe5ss7l24lqnJgcWCSBi8Lwkl8fNR8O-FyrgfkfjJqXAVBIm55LxbUGxxW7pPtJ8jP2hdqKIE3Ue3nJiD9vaGL_CLSTSdcqa1nyFTSBCy1kQlZMO_XwBb7GL5qyMm0stLCptrhMMCyWbjsQDv4XWytSA-u9QvYshHcI5a0LIS-3xf0Q\\\"}\"}, \"javaClass\": \"java.util.Map\"}]}}]}, \"filterParameter\": {\"javaClass\": \"java.util.Map\", \"map\": {}}}]}","mode":"application/json"}}}


r = requests.post(url,headers=headers,data=data)
print(r.status_code)
print(r.text)