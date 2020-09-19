'''
myspider：基础爬虫框架模块

基础爬虫框架主要包括五大模块，分别为：
* 爬虫调度器（SpiderScheduler）：主要负责协调其他四个模块的工作
* URL管理器（UrlManager）：负责管理URL链接
* HTML下载器（HtmlDownloader）：负责下载HTML网页
* HTML解析器（HtmlParser）：从下载的HTML网页中解析出新的URL链接和目标数据
* 数据存储器（DataWriter）：用于将解析出来的目标数据保存到文件或数据库中
'''
import requests
import csv

class UrlManager:
    '''URL管理器：负责管理URL链接'''
    
    # 构造方法
    def __init__(self):
        # 未爬取的URL集合
        self.new_urls = set()
        # 已爬取的URL集合
        self.used_urls = set()
        
    def has_new_url(self):
        '''
        判断是否有待取的URL
        :return: True/False
        '''
        return self.num_of_new_urls() != 0
    
    def add_new_url(self, url):
        '''
        添加新的URL
        :param url: 单个URL
        :return: None
        '''
        if url is None:
            return
        if url not in self.new_urls and url not in self.used_urls:
            self.new_urls.add(url)
    
    def add_new_urls(self, urls):
        '''
        添加多个新的URL
        :param url: 多个URL
        :return: None
        '''
        if urls is None or len(urls) == 0:
            return
        for url in urls:
            self.add_new_url(url)
    
    def get_new_url(self):
        '''
        获取一个未爬取的URL
        :return: str
        '''
        url = self.new_urls.pop()
        self.used_urls.add(url)
        return url
            
    def num_of_new_urls(self):
        '''
        获取未爬取URL的数量
        return: int
        '''
        return len(self.new_urls)
    
    def num_of_used_urls(self):
        '''
        获取已爬取URL的数量
        return: int
        '''
        return len(self.used_urls)

class HtmlDownloader:
    '''
    HTML下载器：下载网页HTML文本
    '''
    def download(self, url):
        '''
        从指定的URL下载HTML文本内容
        :param url: 被下载网页的URL
        :return: str
        '''
        if url is None:
            return None
        user_agent = 'Mozilla/4.0 (compatible); MSIE 5.5; Windows NT)'
        headers = {'User-Agent': user_agent}
        r = requests.get(url, headers=headers)
        if r.status_code == 200:
            r.encoding = 'utf-8'
            return r.text
        return None
    
class HtmlParser:
    '''
    HTML解析器（抽象类）：解析网页，提取URL和数据
    '''
    
    def parse(self, html_content):
        '''
        解析网页内容，抽取URL和数据
        :return: tuple(urls,data)
        '''
        raise NotImplementedError("无法解析：抽象方法HtmlParser.parse()未定义.")

class DataWriter:
    '''
    数据存储器：存储数据到文件或者数据库中
    默认实现，存储为CSV格式
    '''
    def __init__(self, filename):
        self.filename = filename
        self.data_buffer = []
        
    def put(self, data):
        '''
        存放数据
        :param data:要存放的数据(list)
        '''
        self.data_buffer.extend(data)
    
    def get(self):
        '''
        获取数据
        :return: list
        '''
        return self.data_buffer
        
    def save(self):
        '''
        存储数据
        '''
        with open(self.filename, 'a', encoding='utf-8') as f:
            fieldnames = self.data_buffer[0]
            dict_writer = csv.DictWriter(f, fieldnames)
            dict_writer.writeheader()
            dict_writer.writerows(self.data_buffer)

class SpiderScheduler:
    '''
    爬虫调度器：协调上述四个模块，爬取指定的URL列表
    '''
    # 构造方法
    def __init__(self, html_parser = None, data_writer = None):
        self.url_manager = UrlManager()
        self.html_downloader = HtmlDownloader()
        if html_parser is None:
            self.html_parser = HtmlParser()
        else:
            self.html_parser = html_parser
        if data_writer is None:
            self.data_writer = DataWriter("spider_data.csv")
        else:
            self.data_writer = data_writer
    
    def crawl(self, start_urls):
        '''
        从指定的初始URL列表中爬取数据
        '''
        self.url_manager.add_new_urls(start_urls)
        while(self.url_manager.has_new_url()):
            new_url = self.url_manager.get_new_url()
            print('正在爬取：{}'.format(new_url), end='...')
            
            try:
                html_text = self.html_downloader.download(new_url)
                urls, data = self.html_parser.parse(html_text)
                if (urls is not None) and (len(urls)) > 0:
                    self.url_manager.add_new_urls(urls)
                if data is not None:
                    self.data_writer.put(data)
                num_of_used = self.url_manager.num_of_used_urls()
                num_of_new = self.url_manager.num_of_new_urls()
                print('已完成{0}，剩余{1}.'.format(num_of_used, num_of_new))                
            except Exception as e:
                print("发生错误：{}".format(e))
                raise e

        self.data_writer.save()       