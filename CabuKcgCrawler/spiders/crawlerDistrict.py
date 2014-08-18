from scrapy.spider import Spider
from scrapy.selector import Selector

from CabuKcgCrawler.items import CabukcgcrawlerItem

import io,json

class CabuKcgCrawlerDistrict(Spider):
    name = "District"
    allowed_domains = ["gov.tw"]
    start_urls = [
        "http://cabu.kcg.gov.tw/cabu2/statis61B3.aspx"
    ]

    def parse(self, response):
    	sel = Selector(response)
    	items = []

    	districts = sel.xpath('//select[@id="ddlArea"]/option/@value').extract()

    	for district in districts:
    		print district

    	return None