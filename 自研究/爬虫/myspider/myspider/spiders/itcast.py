import scrapy
import logging

logger = logging.getLogger(__name__) #设置log时当前文件名
class ItcastSpider(scrapy.Spider):
    name = "itcast" #爬虫名
    allowed_domains = ['itcast.cn'] #限定爬取范围
    start_urls = ['http://www.itcast.cn/channel/teacher.shtml'] #设置爬取地址


    
    def parse(self, response):#解析
        ret1 = response.xpath("//div[@class='tea_con']//h3/text()").extract()
        # print(ret1)

        li_list = response.xpath("//div[@class='tea_con']//li")

        for i in li_list:
            item = {}
            item["name"] = i.xpath(".//h3/text()").extract_first()
            item["title"] = i.xpath(".//h4/text()").extract_first()
            logger.warning(item)
            yield item #将参数传入pipelines做处理
            