# -*- coding: utf-8 -*-
import scrapy


class HrSpider(scrapy.Spider):
    name = 'hr'
    allowed_domains = ['tencet.com']
    start_urls = ['http://hr.tencet.com/position.php']

    def parse(self, response):
        tr_list = response.xpath("//table[@class='tablelist']/tr")[1:-1]
        print(print(response.text))
