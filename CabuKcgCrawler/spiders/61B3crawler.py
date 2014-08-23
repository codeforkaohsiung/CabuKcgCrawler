# -*- coding: UTF-8 -*-

from scrapy.spider import Spider
from scrapy.selector import Selector
from scrapy.shell import inspect_response

from CabuKcgCrawler.items import CabuKcgVillageData
from CabuKcgCrawler.utils import CabuKcgVillageFactory

import io,json,scrapy,cgi
import HTMLParser


class CabuKcgCrawler61B3(Spider):
  name = "61B3"
  allowed_domains = ["gov.tw"]
  start_urls = [
    "http://cabu.kcg.gov.tw/cabu2/statis61B3.aspx"
  ]

  def __init__(self):
    self.districtData = None
    self.currentDistrict = None
    self.download_delay = 0.5

  def next(self, response):    
    if CabuKcgVillageFactory().hasNext() != True:
      CabuKcgVillageFactory().printSelf()
      return None

    self.districtData = CabuKcgVillageFactory().next()

    if self.districtData['district'] == u'小港區':
      if self.districtData['village'] == u'宏亮里' or self.districtData['village'] == u'店鎮里' or self.districtData['village'] == u'松金里' or self.districtData['village'] == u'桂林里' or self.districtData['village'] == u'廈莊里' or self.districtData['village'] == u'鳳宮里' or self.districtData['village'] == u'鳳源里' or self.districtData['village'] == u'鳳興里' or self.districtData['village'] == u'濟南里':
        inspect_response(response)
        self.addSuffixes()
        #self.districtData = CabuKcgVillageFactory().next()
        #self.districtData['village'] = self.districtData['village'] + u'　'

    if self.districtData['district'] == u'鳳山二':
      if self.districtData['village'] == u'二甲里' or self.districtData['village'] == u'中民里' or self.districtData['village'] == u'中榮里' or self.districtData['village'] == u'天興里' or self.districtData['village'] == u'武漢里' or self.districtData['village'] == u'保安里' or self.districtData['village'] == u'南和里' or self.districtData['village'] == u'國光里' or self.districtData['village'] == u'國富里' or self.districtData['village'] == u'富甲里' or self.districtData['village'] == u'善美里' or self.districtData['village'] == u'新武里' or self.districtData['village'] == u'新強里' or self.districtData['village'] == u'新樂里' or self.districtData['village'] == u'福祥里' or self.districtData['village'] == u'福興里' or self.districtData['village'] == u'鎮南里':
        self.addSuffixes()
        #self.districtData = CabuKcgVillageFactory().next()

    if self.districtData['district'] == u'林園區':
      if self.districtData['village'] == u'西溪里' or self.districtData['village'] == u'東林里' or self.districtData['village'] == u'林家里' or self.districtData['village'] == u'頂厝里' or self.districtData['village'] == u'港嘴里' or self.districtData['village'] == u'鳳芸里' or self.districtData['village'] == u'潭頭里':
        self.addSuffixes()
        #self.districtData = CabuKcgVillageFactory().next()

    if self.districtData['district'] == u'大寮區':
      if self.districtData['village'] == u'上寮里' or self.districtData['village'] == u'山頂里':
        self.addSuffixes()
        #self.districtData = CabuKcgVillageFactory().next()

    if self.districtData['district'] == u'大樹區':
      if self.districtData['village'] == u'和山里' or self.districtData['village'] == u'統嶺里' or self.districtData['village'] == u'興山里' or self.districtData['village'] == u'龍目里':
        self.addSuffixes()
        #self.districtData = CabuKcgVillageFactory().next()

    if self.districtData['district'] == u'大社區':
      if self.districtData['village'] == u'保社里' or self.districtData['village'] == u'嘉誠里' or self.districtData['village'] == u'觀音里':
        self.addSuffixes()
        #self.districtData = CabuKcgVillageFactory().next()

    if self.districtData['district'] == u'路竹區':
      if self.districtData['village'] == u'竹西里' or self.districtData['village'] == u'竹南里' or self.districtData['village'] == u'竹滬里' or self.districtData['village'] == u'社西里' or self.districtData['village'] == u'社南里' or self.districtData['village'] == u'頂寮里' or self.districtData['village'] == u'鴨寮里':
        self.addSuffixes()
        #self.districtData['village'] = self.districtData['village'] + u'　'
        #inspect_response(response)
        #self.districtData = CabuKcgVillageFactory().next()

    if self.districtData['district'] == u'六龜區':
      if self.districtData['village'] == u'荖濃里':
        self.addSuffixes()
        #self.districtData['village'] = self.districtData['village'] + u'　'


    if self.currentDistrict == None or self.currentDistrict != self.districtData['district']:
      self.currentDistrict = self.districtData['district']
      return scrapy.FormRequest.from_response(
        response,
        formdata={'ddlArea': self.currentDistrict, 'LinkButton1': ''},
        callback=self.submitDistrict
      )

    #print "ddlArea = [",self.districtData['district'],"] ddlLi = [", self.districtData['village'], "]. "

    html_parser = HTMLParser.HTMLParser()
    print "ddlArea = [",cgi.escape(self.districtData['district']),"] ddlLi = [", cgi.escape(self.districtData['village']), "]. "
    #inspect_response(response)

    return scrapy.FormRequest.from_response(
            response,
            formname="Form1",
            dont_click=True,
            formdata={'ddlArea': cgi.escape(self.districtData['district']), 'ddlLi': cgi.escape(self.districtData['village'])},
            clickdata={'name': "btnSearch"},
            meta={'http-equiv': "Content-Type", 'content': "text/html; charset: UTF-8"},
            callback=self.submit_district
    )

  def addSuffixes(self):
    self.districtData['village'] = self.districtData['village'] + u'　'

  def parse(self, response):
    with io.open('data/district.json', 'r', encoding='utf-8') as f:
      CabuKcgVillageFactory().loadFromJSON(json.load(f))
    return self.next(response)

  def submitDistrict(self, response):
    return self.next(response)

  def submit_district(self, response):
    sel = Selector(response)
    itemHeader = []
    items = []

    headers = sel.xpath('//table[@id="dgPeopleStatis"]/tr/th/text()')
    for header in headers:
      itemHeader.append(header.extract())

    dates = sel.xpath('//table[@id="dgPeopleStatis"]/tr/td[1]/font/span/text()')
    rols = sel.xpath('//table[@id="dgPeopleStatis"]/tr/td/text()')

    i = 0
    item = None
    dateIter = iter(dates)
    for rol in rols:
      if rol.extract().replace('\r','').replace('\n','').replace('\t','') != "":
        if i % (len(itemHeader) - 1) == 0:
          if item != None:
            items.append(item)
          item = []
          date = next(dateIter)
          item.append(date.extract())
          item.append(rol.extract())
        else:
          item.append(rol.extract())

        i = i + 1
    
    CabuKcgVillageFactory().fillOfData(self.districtData['district'], self.districtData['village'], itemHeader, items)
    #inspect_response(response)

    return self.next(response)