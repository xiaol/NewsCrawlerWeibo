#/usr/bin/env python
#-*-coding=utf-8-*-

'''
Created on Nov 15, 2015
@author :wangzhen
'''
import logging
import sys
import scrapy
from scrapy.http import Request, FormRequest
from weibo.items import WeiboItem, WeiboElement
import os
import sys
import re
import json
import uniout   
from lxml import etree
import xml.etree.ElementTree as ET
from random import randint
from StringIO import StringIO

logger = logging.getLogger('breakingnewsloger')
class BreakingnewsSpider(scrapy.Spider):

    name = 'breakingnews'
    allowed_domains = ['weibo.com']

    def __init__(self):
        self.headers = {'User-Agent':'Mozilla/5.0 (Linux; U; Android 4.3; en-us; SM-N900T Build/JSS15J) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30'}
        #self.url = 'http://m.weibo.cn/page/json?containerid=1005051618051664_-_WEIBO_SECOND_PROFILE_WEIBO&page=1'
        self.url = 'http://m.weibo.cn/page/json?containerid=1005051893801487_-_WEIBO_SECOND_PROFILE_WEIBO&page=1'
    
    def start_requests(self):
        yield FormRequest(self.url, headers = self.headers, callback = self.parser)
    
    def get_img_list(self, mblog, f_img_list):
        if mblog.has_key('thumbnail_pic'):
            img_id_list = mblog['pic_ids']
            thumbnail_pic_url = mblog['thumbnail_pic']
            target_id = thumbnail_pic_url.split('/')[-1].replace('.jpg','')
            for img_id in img_id_list:
                f_img_list.append(thumbnail_pic_url.replace(target_id, img_id))
    
    def list_max_length_str_index(self,str_list):
        max_length_str_index =  0
        max_length = -1
        for i in xrange(len(str_list)):
            if len(str_list[i]) > max_length:
                max_length_str_index = i
                max_length = len(str_list[i])
        return max_length_str_index

    def get_text_from_page(self, html):
        print 100 * '0'
        parser = etree.HTMLParser()
        tree = etree.parse(StringIO(html), parser)
        texts_list = tree.xpath(".//text()")
        index = self.list_max_length_str_index(texts_list)  
        content = texts_list[index].strip()
        print content
        return content

    def parser(self, response):
        weibo_list = []
        try:
            page_json = json.loads(response.body)
            cards = page_json['cards']
            card_list = cards[0]['card_group']
            for card in card_list:
                weibo = WeiboElement()
                weibo.mid = card['mblog']['mid']

                weibo.content = card['mblog']['text']
                if weibo.content.encode('utf-8').startswith('<a class'):    
                    weibo.content = self.get_text_from_page(card['mblog']['text'])
                weibo.created_timestamp = card['mblog']['created_timestamp']
                weibo.reposts_count = card['mblog']['reposts_count']
                weibo.comments_count = card['mblog']['comments_count']
                weibo.like_count = card['mblog']['like_count']
               
                img_list = []
                self.get_img_list(card['mblog'], img_list)
                weibo.img_list = img_list

                if card['mblog'].has_key('page_info'):
                    weibo.title = card['mblog']['page_info']['page_title']
                if card['mblog'].has_key('topic_struct'):
                    weibo.topic = card['mblog']['topic_struct'][0]['topic_title']
                    weibo.topic_url = card['mblog']['topic_struct'][0]['topic_url']
                weibo_list.append(weibo)
        except Exception, e:
            logger.warning(" Exception in parser")
            logger.exception(e)
        weibo_item = WeiboItem()
        weibo_item['weibo_list_item'] = weibo_list
        yield weibo_item
