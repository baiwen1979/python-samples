# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import json

class CnblogspiderPipeline(object):
    
    # 构造函数
    def __init__(self):
        self.file = open('papers.json', 'w')
        
    def process_item(self, item, spider):
        if item['title']:
            line = json.dumps(dict(item)) + '\n'
            self.file.write(line)
            return item
        else:
            raise DropItem("错误：数据项{}缺少标题".format(item))
        
    
