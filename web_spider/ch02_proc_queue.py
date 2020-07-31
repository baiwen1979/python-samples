from multiprocessing import Process, Queue
import os, time, random
import requests
from bs4 import BeautifulSoup

# 生成者(写入数据）进程执行的函数
def producer_put(q, urls):
    print('Producer Process({}) is putting urls:'.format(os.getpid()))
    for url in urls:
        q.put(url)
        print('Putting {} to Queue...'.format(url), end='')
        # time.sleep(random.random() * 5)
        print('Done.')
    print('All Done.')

# 消费者（读取数据）进程执行的函数
def consumer_get(q):
    print('Consumer Process({}) is getting urls:'.format(os.getpid()))
    while True:
        url = q.get(True)
        print('Get {} from Queue.'.format(url))
        crawl(url)
        if q.empty():
            break

def crawl(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh;\
Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) \
Chrome/75.0.3770.100 Safari/537.36'}
    r = requests.get(url, headers = headers)
    r.encoding = 'utf-8'
    if r.ok:
        soup = BeautifulSoup(r.text, 'lxml')
        title = soup.find('title').text.strip()
        print(title)
    
# 主进程执行
def main():
    
    # 创建Queue,并传给各子进程
    q = Queue()

    # 要爬取（消费）的网址列表
    urls = [
        'http://www.baidu.com',
        'http://www.taobao.com',
        'http://www.126.com',
        'https://www.sina.com.cn/',
        'http://www.jd.com',
        'https://www.ifeng.com/'
    ]
    # 创建生产者进程
    producer = Process(target=producer_put, args=(q, urls))
    # 创建消费者进程
    spider1 = Process(target=consumer_get, args=(q,))
    spider2 = Process(target=consumer_get, args=(q,))

    # 启动生产者进程
    producer.start()
    # 启动消费者进程
    spider1.start()
    spider2.start()

    # 等待生产者结束
    producer.join()
    # 等待消费者结束
    spider1.join()
    spider2.join()
    
if __name__ == '__main__':
    main()