import requests
from bs4 import BeautifulSoup
# 指定要爬取的页面URL，并伪装
url = "http://www.w3school.com.cn"
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh;\
Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) \
Chrome/75.0.3770.100 Safari/537.36'} 
# 加载页面
r = requests.get(url, headers = headers)
# 重新编码和解码
if r.ok:
    r.encoding = 'gbk'
    # 准备解析
    soup = BeautifulSoup(r.text, 'lxml')
    div = soup.find('div', id="d1")
    title = div.h2.text.strip()
    print(title)
    with open('title.txt', 'w') as f:
        f.write(title)