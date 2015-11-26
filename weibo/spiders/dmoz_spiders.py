import scrapy
from items import DmozItem
class DmozSpider(scrapy.spiders.Spider):
    name = 'dmoz'
    allowed_domains = ['dmoz.org']

    start_urls = [
            "http://www.baidu.com"
            ]

    def parse(self, response):
            filename = 'baidu'
            with open (filename, 'wb') as f:
                f.write(response.body)
