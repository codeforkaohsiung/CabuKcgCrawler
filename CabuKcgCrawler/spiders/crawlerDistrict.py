from scrapy.spider import Spider
from scrapy.selector import Selector

from CabuKcgCrawler.items import CabukcgcrawlerItem

import io,json,scrapy

class CabuKcgCrawlerDistrict(Spider):
    name = "District"
    allowed_domains = ["gov.tw"]
    start_urls = [
        "http://cabu.kcg.gov.tw/cabu2/statis61B3.aspx"
    ]

    districts = []

    def parse(self, response):
    	sel = Selector(response)

    	districts = sel.xpath('//select[@id="ddlArea"]/option/@value').extract()

    	for district in districts:
    		print district

    	return scrapy.FormRequest.from_response(
    		response,
    		formdata={'ddlArea': districts[2], 'LinkButton1': ''},
    		callback=self.after_login
      )

    def after_login(self, response):
    	sel = Selector(response)

    	villages = sel.xpath('//select[@id="ddlLi"]/option/@value').extract()

    	for village in villages:
    		print village

    	return None