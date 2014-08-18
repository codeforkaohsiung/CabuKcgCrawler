# -*- coding: UTF-8 -*-

from scrapy.spider import Spider
from scrapy.selector import Selector

from CabuKcgCrawler.items import CabukcgcrawlerItem

import io,json,scrapy

class CabuKcgCrawlerDistrict(Spider):
		name = "District"

		def __init__(self):
			self.allowed_domains = ["gov.tw"]
			self.start_urls = ["http://cabu.kcg.gov.tw/cabu2/statis61B3.aspx"]
			self.districts = []
			self.districtsCount = 0
			self.districtsTotal = 0
			self.items = []

		def parse(self, response):
			sel = Selector(response)
			self.districts = sel.xpath('//select[@id="ddlArea"]/option/@value').extract()

			for district in self.districts:
				self.districtsTotal = self.districtsTotal + 1
				#print district

			return scrapy.FormRequest.from_response(
    		response,
    		formdata={'ddlArea': self.districts[self.districtsCount], 'LinkButton1': ''},
    		callback=self.submit_district
      )

		def submit_district(self, response):
			#print "Count = ", self.districtsCount, " Value = ", self.districts[self.districtsCount]

			sel = Selector(response)
			villages = sel.xpath('//select[@id="ddlLi"]/option/@value').extract()
			filterVillages = []
			for village in villages:
				if village != u'合計':
					filterVillages.append(village)

			data = {self.districts[self.districtsCount]: filterVillages}
			self.items.append(data)

			self.districtsCount = self.districtsCount + 1
			if self.districtsCount >= self.districtsTotal:
				self.output()
				return

			return scrapy.FormRequest.from_response(
    		response,
    		formdata={'ddlArea': self.districts[self.districtsCount], 'LinkButton1': ''},
    		callback=self.submit_district
      )

		def output(self):
			print json.dumps(self.items, ensure_ascii=False)
			with io.open('data/district.json', 'w', encoding='utf-8') as f:
				f.write(unicode(json.dumps(self.items, ensure_ascii=False)))
