import scrapy

class mingyan(scrapy.Spider): #继承scrapy.Spider类
    name = "mingyan" #定义蜘蛛名

    def start_requests(self): #此方法爬取页面

        #定义爬取地址
        urls = [
            "http://lab.scrapyd.cn/page/1/",
            "http://lab.scrapyd.cn/page/2/",
        ]

        for url in urls:
            # print(url)
            yield scrapy.Request(url=url,callback=self.parse) #爬取到的页面交给parse处理
        
    def parse(self, response):
        print('*'*40)
        page = response.url.split("/")[-2]     #根据上面的链接提取分页,如：/page/1/，提取到的就是：1
        filename = 'mingyan-%s.html' % page    #拼接文件名，如果是第一页，最终文件名便是：mingyan-1.html
        with open(filename, 'wb') as f:        #python文件操作，不多说了；
            f.write(response.body)             #刚才下载的页面去哪里了？response.body就代表了刚才下载的页面！
        self.log('保存文件: %s' % filename)      # 打个日志
        print('*'*40)


