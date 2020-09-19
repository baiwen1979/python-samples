from scrapy import Spider, Request
from scrapy.selector import Selector
from CNblogSpider.items import CnblogspiderItem

class CnblogsSpider(Spider):
    # 爬虫的名称
    name = "cnblogs"
    allowed_domains = ['cnblogs.com']
    start_urls = ['https://www.cnblogs.com/qiyeboy/']
    
    def parse(self, response):
        papers = response.xpath('.//div[@class="day"]')
        for paper in papers:
            # 提取链接
            link = paper.xpath('.//*[@class="postTitle"]/a/@href')
            link = link.extract()[0].strip()
            # 提取标题
            title = paper.xpath('.//*[@class="postTitle"]/a/text()')
            title = title.extract()[0].strip()
            # 提取时间
            time = paper.xpath('.//*[@class="dayTitle"]/a/text()')
            time = time.extract()[0].strip()
            # 提取摘要
            summary = paper.xpath('.//*[@class="c_b_p_desc"]/text()')
            summary = summary.extract()[0].strip()
            item = CnblogspiderItem(link=link, title=title, 
                                    time=time, summary=summary)
            yield item
            
        next_page = Selector(response).re(u'<a href="(\S*)">\s*下一页\s*</a>')
        if next_page:
            yield Request(url=next_page[0], callback=self.parse)
