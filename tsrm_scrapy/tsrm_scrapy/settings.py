# Scrapy settings for tsrm_scrapy project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#
#import os
#PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

import sys
sys.path.append('/ttrack/tsrm-app')

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tsrm.settings")

BOT_NAME = 'tsrm_scrapy'

SPIDER_MODULES = [ 'tsrm_scrapy.spiders']
NEWSPIDER_MODULE = 'tsrm_scrapy.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64; rv:24.0) Gecko/20100101 Firefox/24.0'

ITEM_PIPELINES = {
    'tsrm_scrapy.pipelines.TsrmScrapyPipeline': 1000,
}
DOWNLOADER_MIDDLEWARES = {
    #'scrapy.contrib.downloadermiddleware.httpcache.HttpCacheMiddleware': 300,
}

HTTPCACHE_ENABLED = True
HTTPCACHE_DIR = '/ttrack/tsrm-app/tsrm_scrapy/httpcache'

HTTPCACHE_POLICY = 'scrapy.contrib.httpcache.DummyPolicy'

HTTPCACHE_IGNORE_MISSING = False
HTTPCACHE_STORAGE = 'scrapy.contrib.httpcache.FilesystemCacheStorage'
#DUPEFILTER_CLASS = 'scraper.duplicate_filter.NullDupeFilter'
#DUPEFILTER_CLASS = 'scrapy.dupefilter.basedupefilter'
