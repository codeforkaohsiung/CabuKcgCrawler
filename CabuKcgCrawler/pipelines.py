# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy import log
from CabuKcgCrawler.utils import CabuKcgVillageFactory

import io,json

class DistrictJSONWritePipeline(object):
	name = "DistrictJSONWritePipeline"

	def __init__(self):
		self.rawItems = []
		self.clearItems = []
		self.SamiDistrict = []
		self.FonsanDistrict = []

	def isExecute(self, spider):
		if 'DistrictJSONWritePipeline' in getattr(spider, 'pipelines'):
			log.msg('[DistrictJSONWritePipeline] is skip this step.', level=log.DEBUG)
			return True

		return False

	def process_item(self, item, spider):
		if self.isExecute(spider) is not True:
			return item

		if u'三民' in item['district']:
			if item['district'] != u'三民區':
				it = {'district': item['district'], 'villages': item['villages']}
				self.rawItems.append(it)
			
			item.stripData()
			for v in item['villages']:
				self.SamiDistrict.append(v)
			return item

		if u'鳳山' in item['district']:
			it = {'district': item['district'], 'villages': item['villages']}
			self.rawItems.append(it)

			item.stripData()
			for v in item['villages']:
				log.msg('Village: [{0}]'.format(v.encode('utf-8')), level=log.DEBUG)
				self.FonsanDistrict.append(v)
			return item

		log.msg('[DistrictJSONWritePipeline] Process JSON Output...', level=log.DEBUG)
		it = {'district': item['district'], 'villages': item['villages']}
		self.rawItems.append(it)
		
		item.stripData()
		it = {'district': item['district'], 'villages': item['villages']}
		self.clearItems.append(it)

		return item

	def close_spider(self, spider):
		if self.isExecute(spider) is not True:
			return None

		it = {'district': u'三民區', 'villages': self.SamiDistrict}
		self.clearItems.append(it)


		it = {'district': u'鳳山區', 'villages': self.FonsanDistrict}
		self.clearItems.append(it)

		log.msg('[DistrictJSONWritePipeline] spider is close.', level=log.INFO)
		with io.open('data/raw/district.json', 'w', encoding='utf-8') as f:
			f.write(unicode(json.dumps(self.rawItems, indent=2, sort_keys=True, ensure_ascii=False)))

		with io.open('data/clear/district.json', 'w', encoding='utf-8') as f:
			f.write(unicode(json.dumps(self.clearItems, indent=2, sort_keys=True, ensure_ascii=False)))


class C61B3JSONWritePipeline(object):
	name = "C61B3JSONWritePipeline"

	def __init__(self):
		self.rawItems = []
		self.clearItems = []
		self.SamiDistrict = []
		self.FonsanDistrict = []

	def isExecute(self, spider):
		if 'C61B3JSONWritePipeline' in getattr(spider, 'pipelines'):
			log.msg('[C61B3JSONWritePipeline] is skip this step.', level=log.DEBUG)
			return True

		return False

	def process_item(self, item, spider):
		if self.isExecute(spider) is not True:
			return item

	def close_spider(self, spider):
		if self.isExecute(spider) is not True:
			return None

		CabuKcgVillageFactory().printSelf()