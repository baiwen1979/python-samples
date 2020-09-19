# -*- coding: utf-8 -*-
import scrapy, re
from scrapy import Request
from XiaozhuSpider.items import XiaozhuspiderItem

class XiaozhuSpider(scrapy.Spider):
    name = 'xiaozhu'
    allowed_domains = ['xiaozhu.com']
    start_urls = ['http://ty.xiaozhu.com/search-duanzufang-p1-0/']

    def parse(self, response):
        
        # 内部函数
        def get_next_url(response):
            url_pattern = re.compile(r'\S*p(\d+)\S*')
            page_number_pattern = re.compile(r'p\d+')
            page_number = int(re.search(url_pattern, response.url).group(1))
            next_url = re.sub(page_number_pattern, 
                              'p' + str(page_number + 1), response.url)
            if page_number == 5:
                return None
            else:
                return next_url
            
        house_divs = response.xpath('.//div[@class="result_intro"]')
        for house_div in house_divs: 
            title_span = house_div.xpath('./a/span/text()') 
            title = title_span.extract()[0].strip() 
            desc_em = house_div.xpath('./em/text()')
            desc = desc_em.extract()[0].strip()
            comment_span = house_div.xpath('./em/span/text()')
            comment = comment_span.extract()[0].strip() 
            comment = comment.strip('-').strip()
            item = XiaozhuspiderItem(title=title,desc=desc,comment=comment)
            yield item
        
        next_page_url = response.xpath('.//a[@class="font_st"][last()]/@href').extract()[0]
        if next_page_url:
            yield Request(next_page_url, callback=self.parse)
            