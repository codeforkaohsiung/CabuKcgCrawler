# -*- coding: utf-8 -*-


from scrapy.item import Item, Field
from scrapy import log
from utils import CabuKcgVillageFactory

import string

class CabuKcgDistrictItem(Item):
  district = Field()
  villages = Field()
  header = Field()
  data = Field()

  def stripData(self):
    items = []
    for v in self['villages']:
      #log.msg('Befare strip: [{0}]'.format(v.encode('utf-8')), level=log.DEBUG)
      v = string.replace(v, u'　', '')
      v = string.replace(v, '\u3000', '')
      v.strip()
      #log.msg('After strip: [{0}]'.format(v.encode('utf-8')), level=log.DEBUG)
      items.append(v)

    self['villages'] = items

  def __str__(self):
    return '[{0} - {1}] Data => {2}'.format(unicode(self['district']).encode('utf-8'), unicode(self['village']).encode('utf-8'), self['data'])

    
class CabuKcgVillageData(Item):
  district = Field()
  village = Field()
  headers = Field()
  data = Field()

  def __str__(self):
    return '[{0} - {1}] Data => {2}'.format(unicode(self['district']).encode('utf-8'), unicode(self['village']).encode('utf-8'), self['data'])