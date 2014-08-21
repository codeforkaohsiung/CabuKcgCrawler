# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field


class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class CabukcgcrawlerItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = Field()
    description = Field()
    url = Field()

class CabuKcgVillageFactory:
    __metaclass__ = Singleton

    def __init__(self):
    	pass

    def loadFromJSON(self, villages):
    	for district in villages:
    		keys = district.iterkeys()
    		for key in keys:
    			for v in district[key]:
    				item = CabuKcgVillageData()
    				item['district'] = key
    				item['village'] = v
    				print item

    	return None

class CabuKcgVillageData(Item):
	district = Field()
	village = Field()

	def __str__(self):
		return '[{0} - {1}]'.format(unicode(self['district']).encode('utf-8'), unicode(self['village']).encode('utf-8'))