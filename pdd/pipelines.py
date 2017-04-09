# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


import json
import codecs

class PddPipeline(object):
    
    def open_spider(self, spddpider):
        self.file = codecs.open('items.json', 'wb', encoding='utf-8')
    
    def process_item(self, item, spddpider):
        line = json.dumps(dict(item), ensure_ascii=False) + "\n"
        self.file.write(line)
        return item
    
    def close_spider(self, spddpider):
        self.file.close()
