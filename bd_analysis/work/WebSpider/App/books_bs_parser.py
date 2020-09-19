'''
基于BeautifulSoup和JSON的HTML静态页面解析和数据存储模块
'''
from bs4 import BeautifulSoup
import json

def parse_books(html_text):
    '''从HTML文本中解析出所有图书列表'''
    soup = BeautifulSoup(html_text, 'lxml')
    books = []
    book_divs = soup.find_all('div', class_="mulu")
    
    for book_div in book_divs:
        h2 = book_div.find('h2')
        if h2 != None:
            book_title = h2.text # 获取标题
            links = book_div.find_all('a')
            chapters = parse_chapters(links)
            books.append({'book_title': book_title, 'chapters': chapters})
        
        def parse_chapters(links):
            chapters = []
            for link in links:       
                href = link.get('href')
                title = link.get('title')
                chapters.append({'href':href, 'title':title})
            return chapters
    
    return books

def save_books(filename, books):
    '''将图书列表保存到JSON文件中'''
    with open(filename, 'w') as f:
            json.dump(books, fp = f, indent = 4)