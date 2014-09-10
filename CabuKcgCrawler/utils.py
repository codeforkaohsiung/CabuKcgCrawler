# -*- coding: utf-8 -*-


from patterns import Singleton
from scrapy import log

import pprint


class CabuKcgDataItem():
  district = None
  village = None
  headers = None
  data = None


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

class CabuKcgVillageFactory:
  __metaclass__ = Singleton

  def __init__(self):
    self.items = []
    self.processPoint = None

  def loadFromJSON(self, jsons):
    for js in jsons:
      district = js['district']
      villages = js['villages']

      for v in villages:
        item = CabuKcgDataItem()
        item.district = district
        item.village = v
        self.items.append(item)

    self.processPoint = HasNextWrapper(self.items)    

  def hasNext(self):
    return self.processPoint.hasNext()

  def next(self):
    return self.processPoint.next()

  def printSelf(self):
    pp = pprint.PrettyPrinter()
    print "OK, Let's print all object ==>"
    for item in self.items:
      print "[",item.district," (",item.village,") ]"
      pp.pprint(item.headers)
      pp.pprint(item.data)

  def fillOfData(self, district, village, headers, data):
    for it in self.items:
      if it.district == district and it.village == village:
        it.headers = headers
        it.data = data
        break