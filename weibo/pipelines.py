# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

class WeiboPipeline(object):
    def __init__(self):
        print 'initialize file object sucess'

    def process_item(self, item, spider):
        print 1000 *'^'
        line = item['weibo_list_item'][0].content
        print line
        print 1000 *'^'
        return item
