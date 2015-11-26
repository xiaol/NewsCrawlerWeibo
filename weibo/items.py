# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class WeiboItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    mid = scrapy.Field()
    news_content = scrapy.Field()
    news_time = scrapy.Field()
    news_url = scrapy.Field()
    news_title = scrapy.Field()
    news_mid = scrapy.Field()
    news_refer_num = scrapy.Field()
    news_comment_num = scrapy.Field()
    news_like_num = scrapy.Field()
    news_comment = scrapy.Field()
    news_img_url = scrapy.Field()
    comments = scrapy.Field()
    pass

class DmozItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    link = scrapy.Field()
    desc = scrapy.Field()
    pass
