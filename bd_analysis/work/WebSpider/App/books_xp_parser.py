'''
基于lxml和CSV的HTML静态页面解析和数据存储模块
'''
from lxml import etree
import re, csv

def parse_books(html_text):
    '''
    从HTML文本中解析出所有图书列表
    '''
    tree = etree.HTML(html_text)
    book_divs = tree.xpath('.//div[@class="mulu"]')
    pattern = re.compile(r'\s*\[(.*)\]\s+(.*)')
    rows = []
    
    def parse_row(book_title, links):
        href = link.xpath('./@href')[0]
        title = link.xpath('./@title')[0]
        match = re.search(pattern, title)
        if match != None:
            date = match.group(1)
            title = match.group(2)
            row = (book_title, title, href, date)
            return row
        else:
            return None
        
    for book_div in book_divs:
        div_h2 = book_div.xpath('./div/center/h2/text()')
        if (len(div_h2) > 0):
            book_title = div_h2[0]
            # print(book_title)
            links = book_div.xpath('./div/ul/li/a')
            for link in links:
                row = parse_row(book_title,link)
                if row:
                    rows.append(row)
    return rows

def save_books(filename, books):
    '''
    将图书列表保存到CSV文件中
    '''
    # 构造表头
    header = ('book_title', 'title', 'href', 'date')
    # 存储为CSV文件
    with open(filename, 'w') as f:
        csv_writer = csv.writer(f,)
        csv_writer.writerow(header)
        csv_writer.writerows(books)