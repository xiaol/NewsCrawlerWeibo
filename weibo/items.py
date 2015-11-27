# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Item

class WeiboElement(object):
    def __init__(self):
        self.mid = ''
        self.title = ''
        self.topic = ''
        self.topic_url = ''
        self.content = ''
        self.created_timestamp = ''  
        self.img_list = []
        self.reposts_count = 0
        self.comments_count = 0
        self.like_count = 0
        
class WeiboItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    weibo_list_item = scrapy.Field()
