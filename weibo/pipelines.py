# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

class WeiboPipeline(object):
    def __init__(self):
        print 'initialize file object sucess'
        self.fileobj = open('items.txt', 'w+')

    def process_item(self, item, spider):
        print 1000 *'^'
        line = item['news_content'].encode('utf-8')+'\n'
        try:
            self.fileobj.write(line)
            print 'write success'
        except Exception, e:
            print e
        print line
        print 1000 *'^'
        return item
