#/usr/bin/env python
#-*-coding=utf-8-*-

'''
Created on Nov 15, 2015
@author :wangzhen
'''

import sys
import scrapy
from scrapy.http import Request, FormRequest
from weibo.items import WeiboItem, ListElement
import os
import sys
import re
import json
import uniout   
from lxml import etree
import xml.etree.ElementTree as ET
from random import randint

class BreakingnewsSpider(scrapy.Spider):

    name = 'rmrb'
    allowed_domains = ['weibo.com']

    def __init__(self):
        self.headers = {'User-Agent':'Mozilla/5.0 (Linux; U; Android 4.3; en-us; SM-N900T Build/JSS15J) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30'}
        self.url = 'http://m.weibo.cn/page/json?containerid=1005052803301701_-_WEIBO_SECOND_PROFILE_WEIBO&page=1'
    
    def start_requests(self):
        yield FormRequest(self.url, headers = self.headers, callback = self.parser)
    
    def get_img_list(self, mblog, f_img_list):
        if mblog.has_key('thumbnail_pic'):
            img_id_list = mblog['pic_ids']
            thumbnail_pic_url = mblog['thumbnail_pic']
            target_id = thumbnail_pic_url.split('/')[-1].replace('.jpg','')
            for img_id in img_id_list:
                f_img_list.append(thumbnail_pic_url.replace(target_id, img_id))

    def parser(self, response):
        page_json = json.loads(response.body)
        cards = page_json['cards']
        card_list = cards[0]['card_group']
        elements_list = []
        for card in card_list:
            list_element = ListElement()
            list_element.mid = card['mblog']['mid']
            list_element.content = card['mblog']['text']
            list_element.created_timestamp = card['mblog']['created_timestamp']
            list_element.reposts_count = card['mblog']['reposts_count']
            list_element.comments_count = card['mblog']['comments_count']
            list_element.like_count = card['mblog']['like_count']
           
            img_list = []
            self.get_img_list(card['mblog'], img_list)
            list_element.img_list = img_list

            if card['mblog'].has_key('page_info'):
                list_element.title = card['mblog']['page_info']['page_title']
            if card['mblog'].has_key('topic_struct'):
                list_element.topic = card['mblog']['topic_struct'][0]['topic_title']
                list_element.topic_url = card['mblog']['topic_struct'][0]['topic_url']
            print list_element
            elements_list.append(list_element)

        weibo_item = WeiboItem()
        print type(weibo_item)
        weibo_item['element'] = elements_list
        yield weibo_item
