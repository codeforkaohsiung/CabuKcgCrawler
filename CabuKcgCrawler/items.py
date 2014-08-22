# -*- coding: utf-8 -*-


from scrapy.item import Item, Field
from patterns import Singleton

import string

class CabuKcgDistrictItem(Item):
  district = Field()
  villages = Field()

  def stripData(self):
    for v in self['villages']:
      v = string.replace(v, u'　', '')
      v.strip()


class HasNextWrapper(object):

  def __init__(self, it):
    self.it = iter(it)
    self._hasnext = None

  def __iter__(self): return self
    
  def next(self):
    if self._hasnext:
      result = self._thenext
    else:
      result = next(self.it)
    
    self._hasnext = None    
    return result

  def hasNext(self):
    if self._hasnext is None:
      try: 
        self._thenext = next(self.it)
        self._hasnext = True
      except StopIteration: 
        self._hasnext = False
    
    return self._hasnext


class CabukcgcrawlerItem(Item):
  name = Field()
  description = Field()
  url = Field()

class CabuKcgVillageFactory:
  __metaclass__ = Singleton

  def __init__(self):
    self.items = []
    self.processPoint = None

  def loadFromJSON(self, villages):
    for district in villages:
      keys = district.iterkeys()
      
      for key in keys:
        for v in district[key]:
          item = CabuKcgVillageData()
          item['district'] = key
          item['village'] = v
          item['headers'] = None
          item['data'] = None
          self.items.append(item)

      self.processPoint = HasNextWrapper(self.items)    

  def hasNext(self):
    return self.processPoint.hasNext()

  def next(self):
    return self.processPoint.next()

  def printSelf(self):
    print "OK, Let's print all object ==>"
    for item in self.items:
      print item

  def fillOfData(self, district, village, headers, data):
    for it in self.items:
      if it['district'] == district and it['village'] == village:
        it['headers'] = headers
        it['data'] = data
        print it
        break


class CabuKcgVillageData(Item):
  district = Field()
  village = Field()
  headers = Field()
  data = Field()


  def __str__(self):
    return '[{0} - {1}] Data => {2}'.format(unicode(self['district']).encode('utf-8'), unicode(self['village']).encode('utf-8'), self['data'])