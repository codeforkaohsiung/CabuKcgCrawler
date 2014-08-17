from scrapy.spider import Spider
from scrapy.selector import Selector

from CabuKcgCrawler.items import CabukcgcrawlerItem


class CabuKcgCrawler61B3(Spider):
    name = "61B3"
    allowed_domains = ["gov.tw"]
    start_urls = [
        "http://cabu.kcg.gov.tw/cabu2/statis61B3.aspx"
    ]

    def parse(self, response):
        """
        The lines below is a spider contract. For more info see:
        http://doc.scrapy.org/en/latest/topics/contracts.html

        @url http://cabu.kcg.gov.tw/cabu2/statis61B3.aspx
        @scrapes name
        """
        sel = Selector(response)
        headers = sel.xpath('//table[@id="dgPeopleStatis"]/tr[1]/th/text()')
        print "-- Table headers"
        for header in headers:
            print header.extract()

        rols = sel.xpath('//table[@id="dgPeopleStatis"]/tr/td/text()')
        items = []

#        for rol in rols:
#            item = Website()
#            item['name'] = site.xpath('a/text()').extract()
#            item['url'] = site.xpath('a/@href').extract()
#            item['description'] = site.xpath('text()').re('-\s([^\n]*?)\\n')
#            items.append(item)

        return items
