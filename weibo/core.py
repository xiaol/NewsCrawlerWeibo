#!/usr/bin python

# import the spiders ypu want to run
from spiders.breakingnews_spiders import BreakingnewsSpider
from spiders.rmrb_spiders import RmrbSpider
from spiders.dmoz_spiders import DmozSpider
from scrapy.utils.project import get_project_settings
#scrapy api imports
from scrapy import signals
from twisted.internet import reactor
from scrapy.crawler import Crawler
from scrapy.settings import Settings

#list of crawlers
TO_CRAWL = [BreakingnewsSpider, DmozSpider, RmrbSpider]

# crawlers that are running

RUNNING_CRAWLERS=[]
def spider_closing(spider):
    """
    Activates on spider closed signal
    """

    #log.msg("Spider closed :%s "%spider, level = log.INFO)
    RUNNING_CRAWLERS.remove(spider)
    if not RUNNING_CRAWLERS:
        reactor.stop()
    
# start logger
#log.start(loglevel = log.DEBUG)

# set up the crawler and start to crawl one spider at a time
for spider in TO_CRAWL:
    if spider is not DmozSpider:
        settings = get_project_settings()
    else:
        settings.set("USER_AGENT", "Kiran Koduru (+http://kirankoduru.github.io)")
    crawler = Crawler(spider,settings)
    crawler_obj = spider()
    RUNNING_CRAWLERS.append(crawler_obj)

    #stop reactor when spider closes
    crawler.signals.connect(spider_closing, signal=signals.spider_closed)
    #crawler.configure()
    crawler.crawl(crawler_obj)
    print type(crawler)
    #crawler.start()

# blocks process; so always keep as the last  statement
reactor.run()
