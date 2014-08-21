# -*- coding: UTF-8 -*-

from scrapy.spider import Spider
from scrapy.selector import Selector
from scrapy.shell import inspect_response

from CabuKcgCrawler.items import CabuKcgVillageData, CabuKcgVillageFactory

import io,json,scrapy,cgi
import HTMLParser


class CabuKcgCrawler61B3(Spider):
  name = "61B3"
  allowed_domains = ["gov.tw"]
  start_urls = [
    "http://cabu.kcg.gov.tw/cabu2/statis61B3.aspx"
  ]
  #rate = 1

  def __init__(self):
    self.districtData = None
    self.currentDistrict = None
    #self.download_delay = 0.25

  def next(self, response):    
    if CabuKcgVillageFactory().hasNext() != True:
      CabuKcgVillageFactory().printSelf()
      return None

    self.districtData = CabuKcgVillageFactory().next()
    if self.currentDistrict == None or self.currentDistrict != self.districtData['district']:
      self.currentDistrict = self.districtData['district']
      return scrapy.FormRequest.from_response(
        response,
        formdata={'ddlArea': self.currentDistrict, 'LinkButton1': ''},
        callback=self.submitDistrict
      )

    #sel = Selector(response)
    #viewState = sel.xpath('//input[@id="__VIEWSTATE"]/@value').extract()
    #eventValidation = sel.xpath('//input[@id="__EVENTVALIDATION"]/@value').extract()
    print "ddlArea = [",self.districtData['district'],"] ddlLi = [", self.districtData['village'], "]. "

    #if self.districtData['village'] == "山下里":
    #  print "Skip"
    #  self.districtData = CabuKcgVillageFactory().next()
    #  print "ddlArea = [",self.districtData['district'],"] ddlLi = [", self.districtData['village'], "]. "      

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