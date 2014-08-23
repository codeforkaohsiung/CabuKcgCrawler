# -*- coding: utf-8 -*-

# Scrapy settings for CabuKcgCrawler project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'CabuKcgCrawler'

SPIDER_MODULES = ['CabuKcgCrawler.spiders']
NEWSPIDER_MODULE = 'CabuKcgCrawler.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'CabuKcgCrawler (+http://www.yourdomain.com)'
#DEPTH_LIMIT = 1

COOKIES_ENABLES = False

#LOG_LEVEL = 'INFO'

ITEM_PIPELINES = {  
  'CabuKcgCrawler.pipelines.DistrictJSONWritePipeline': 300
} 

#use new useragent
DOWNLOADER_MIDDLEWARES = {
        'scrapy.contrib.downloadermiddleware.useragent.UserAgentMiddleware' : None,
        'CabuKcgCrawler.spiders.rotateUserAgent.RotateUserAgentMiddleware' : 400
}
    		#'scrapy.contrib.downloadermiddleware.retry.RetryMiddleware': None,
    		#'middlewares.MyRetryMiddleware': 500,