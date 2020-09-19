# -*- coding: utf-8 -*-
import scrapy


class CnblogbodySpider(scrapy.Spider):
    name = 'cnblogBody'
    allowed_domains = ['cnblogs.com']
    start_urls = ['http://cnblogs.com/']

    def parse(self, response):
        pass
