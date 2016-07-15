import sys
sys.path.append('/ttrack/tsrm-app/tsrm_scrapy')
sys.path.append('/ttrack/tsrm-app')
from twisted.internet import reactor
from scrapy.crawler import Crawler
from scrapy import log, signals
from tsrm_scrapy.spiders.ticket_spider import TicketSpider
from scrapy.utils.project import get_project_settings

spider = TicketSpider()
settings = get_project_settings()
crawler = Crawler(settings)
crawler.signals.connect(reactor.stop, signal=signals.spider_closed)
crawler.configure()
crawler.crawl(spider)
crawler.start()
log.start()
print log,dir(log)
reactor.run()
