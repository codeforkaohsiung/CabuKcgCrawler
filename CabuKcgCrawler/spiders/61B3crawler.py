# -*- coding: UTF-8 -*-

from scrapy.spider import Spider
from scrapy.selector import Selector
from scrapy.shell import inspect_response

from CabuKcgCrawler.utils import CabuKcgDataItem, CabuKcg61B3TableRow
from CabuKcgCrawler.utils import CabuKcgVillageFactory, CabuKcgStringProcess

import pprint

import io
import json
import scrapy
import HTMLParser


class CabuKcgCrawler61B3(Spider):
    name = "61B3"
    allowed_domains = ["gov.tw"]
    start_urls = ["http://cabu.kcg.gov.tw/cabu2/statis61B3.aspx"]
    pipelines = ["C61B3JSONWritePipeline"]

    def __init__(self):
        self.districtItems = []
        self.districtData = None
        self.currentDistrict = None
        self.download_delay = 0.5

    def next(self, response):
        #pprint(self.districtItems)
        #CabuKcgVillageFactory().printSelf()
        #inspect_response(response)

        if CabuKcgVillageFactory().hasNext() is not True:
            return None

        self.districtData = CabuKcgVillageFactory().next()

        if self.currentDistrict is None or \
                self.currentDistrict is not self.districtData.district:
            self.currentDistrict = self.districtData.district

        return scrapy.FormRequest.from_response(
            response,
            formdata={'ddlArea': self.currentDistrict, 'LinkButton1': ''},
            callback=self.changeDistrict
        )

        #html_parser = HTMLParser.HTMLParser()
        print "ddlArea = [", self.districtData.district, \
            "] ddlLi = [", self.districtData.village, "]. "

        return scrapy.FormRequest.from_response(
            response,
            formname="Form1",
            dont_click=True,
            formdata={'ddlArea': self.districtData.district,
                        'ddlLi': self.districtData.village},
            clickdata={'name': "btnSearch"},
            meta={'http-equiv': "Content-Type",
                     'content': "text/html; charset: UTF-8"},
            callback=self.submit
        )

    def changeDistrict(self, response):
        #print "ddlArea = [",self.districtData['district'],"] ddlLi = [", self.districtData['village'], "]. "

        html_parser = HTMLParser.HTMLParser()
        print "ddlArea = [",self.districtData.district,"] ddlLi = [",self.districtData.village,"]. "
        #inspect_response(response)

        return scrapy.FormRequest.from_response(
            response,
            formname="Form1",
            dont_click=True,
            formdata={'ddlArea': self.districtData.district, 'ddlLi': self.districtData.village},
            clickdata={'name': "btnSearch"},
            meta={'http-equiv': "Content-Type", 'content': "text/html; charset: UTF-8"},
            callback=self.submit)

    def parse(self, response):
        with io.open('data/raw/district.json', 'r', encoding='utf-8') as f:
            CabuKcgVillageFactory().loadFromJSON(json.load(f))
            f.close()
        return self.next(response)

    def submit(self, response):
        sel = Selector(response)
        itemHeader = []
        items = []

        headers = sel.xpath('//table[@id="dgPeopleStatis"]/tr/th/text()')
        for header in headers:
            itemHeader.append(header.extract())

        dates = sel.xpath(
            '//table[@id="dgPeopleStatis"]/tr/td[1]/font/span/text()')
        rols = sel.xpath('//table[@id="dgPeopleStatis"]/tr/td/text()')

        item = CabuKcg61B3TableRow()
        #dateIter = iter(dates)

        for x in xrange(0, len(dates)):
            item.date = CabuKcgStringProcess().cleanTab(dates[x].extract())

            item.numberOfLin = CabuKcgStringProcess() \
                .cleanTab(rols[3+(5*x)].extract())

            item.numberOfFu = CabuKcgStringProcess() \
                .cleanTab(rols[4+(5*x)].extract())

            item.maleNumber = CabuKcgStringProcess() \
                .cleanTab(rols[6+(5*x)].extract())

            item.femaleNumber = CabuKcgStringProcess() \
                .cleanTab(rols[7+(5*x)].extract())

            items.append(item)
            inspect_response(response)

        for rol in rols:
            cleanRol = CabuKcgStringProcess().cleanTab(rol.extract())
            if len(cleanRol) is not 0:
                if i % (len(itemHeader) - 1) == 0:
                    if item is not None:
                        items.append(item)

                    item = CabuKcg61B3TableRow()
                    date = next(dateIter)

                    item.date = date.extract()
                    item.append(cleanRol)

                else:
                    item.append(cleanRol)

            i = i + 1
        CabuKcgVillageFactory().fillOfData(
            self.districtData.district, self.districtData.village,
            itemHeader, items)
        CabuKcgVillageFactory().printSelf()
        inspect_response(response)

        return self.next(response)