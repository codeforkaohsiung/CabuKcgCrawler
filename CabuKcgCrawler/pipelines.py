# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy import log

import io,json

class DistrictJSONWritePipeline(object):
	name = "DistrictJSONWritePipeline"

	def __init__(self):
		self.rawItems = []
		self.clearItems = []

	def process_item(self, item, spider):
		if 'DistrictJSONWritePipeline' not in getattr(spider, 'pipelines'):
			log.msg('[DistrictJSONWritePipeline] Skip', level=log.DEBUG)
			return item

		log.msg('[DistrictJSONWritePipeline] Process...', level=log.DEBUG)
		it = {'district': item['district'], 'villages': item['villages']}
		self.rawItems.append(it)
		
		item.stripData()
		it = {'district': item['district'], 'villages': item['villages']}
		self.clearItems.append(it)

		return item

	def close_spider(self, spider):
		log.msg('[DistrictJSONWritePipeline] spider is close.', level=log.INFO)
		with io.open('data/raw/district.json', 'w', encoding='utf-8') as f:
			f.write(unicode(json.dumps(self.rawItems, indent=2, sort_keys=True, ensure_ascii=False)))

		with io.open('data/clear/district.json', 'w', encoding='utf-8') as f:
			f.write(unicode(json.dumps(self.clearItems, indent=2, sort_keys=True, ensure_ascii=False)))
