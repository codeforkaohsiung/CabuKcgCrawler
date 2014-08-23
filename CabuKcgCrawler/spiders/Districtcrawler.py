# -*- coding: UTF-8 -*-

from scrapy.spider import Spider
from scrapy.selector import Selector

from CabuKcgCrawler.items import CabuKcgDistrictItem

import scrapy

class CabuKcgCrawlerDistrict(Spider):
		name = "District"
		allowed_domains = ["gov.tw"]
		start_urls = ["http://cabu.kcg.gov.tw/cabu2/statis61B3.aspx"]
		pipelines = ["DistrictJSONWritePipeline"]

		def __init__(self):
			self.districts = []
			self.districtsCount = 0
			self.items = []

		def parse(self, response):
			sel = Selector(response)
			self.districts = sel.xpath('//select[@id="ddlArea"]/option/@value').extract()

			return scrapy.FormRequest.from_response(
    		response,
    		formdata={'ddlArea': self.districts[self.districtsCount], 'LinkButton1': ''},
    		callback=self.submit_district
      )

		def submit_district(self, response):
			it = CabuKcgDistrictItem()
			sel = Selector(response)

			villages = sel.xpath('//select[@id="ddlLi"]/option/@value').extract()
			filterVillages = []
			for village in villages:
				if village != u'合計':
					filterVillages.append(village)

			it['district'] = self.districts[self.districtsCount]
			it['villages'] = filterVillages

			self.items.append(it)

			self.districtsCount = self.districtsCount + 1
			if self.districtsCount >= len(self.districts):
				return self.items

			return scrapy.FormRequest.from_response(
    		response,
    		formdata={'ddlArea': self.districts[self.districtsCount], 'LinkButton1': ''},
    		callback=self.submit_district
      )
