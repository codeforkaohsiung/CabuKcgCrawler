from scrapy.spider import Spider
from scrapy.selector import Selector

from CabuKcgCrawler.items import CabuKcgVillageData, CabuKcgVillageFactory

import io,json,scrapy

class CabuKcgCrawler61B3(Spider):
  name = "61B3"
  allowed_domains = ["gov.tw"]
  start_urls = [
    "http://cabu.kcg.gov.tw/cabu2/statis61B3.aspx"
  ]
  rate = 1

  def __init__(self):
    self.districtData = None
    self.download_delay = 2

  def next(self, response):    
    if CabuKcgVillageFactory().hasNext() != True:
      CabuKcgVillageFactory().printSelf()
      return None

    self.districtData = CabuKcgVillageFactory().next()
    print "ddlArea = [",self.districtData['district'],"] ddlLi = [", self.districtData['village'], "]. "
    return scrapy.FormRequest.from_response(
            response,
            formdata={'ddlArea': self.districtData['district'], 'ddlLi': self.districtData['village']},
            callback=self.submit_district
    )


  def parse(self, response):
    with io.open('data/district.json', 'r', encoding='utf-8') as f:
      CabuKcgVillageFactory().loadFromJSON(json.load(f))
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
    return self.next(response)