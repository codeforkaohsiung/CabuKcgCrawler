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

        totalcols = 0
        headers = sel.xpath('//table[@id="dgPeopleStatis"]/tr[1]/th/text()')
        print "-- Table headers --"
        for header in headers:
            print header.extract()
            totalcols = totalcols + 1

        dates = sel.xpath('//table[@id="dgPeopleStatis"]/tr/td[1]/font/span/text()')
        rols = sel.xpath('//table[@id="dgPeopleStatis"]/tr/td/text()')
        print "Total Cols = ", totalcols
        i = 0
        dateIter = iter(dates)
        print "-- Table content --"
        for rol in rols:
        	if rol.extract().replace('\r','').replace('\n','').replace('\t','') != "":
        		#print "Col = ",i
        		if i % (totalcols-1) == 0:
        			date = next(dateIter)
        			print date.extract()
        			print rol.extract()
        		else:
        			print rol.extract()
        		i = i + 1
        	#else:
        	#	print "Remove: ",rol


        items = []

#        for rol in rols:
#            item = Website()
#            item['name'] = site.xpath('a/text()').extract()
#            item['url'] = site.xpath('a/@href').extract()
#            item['description'] = site.xpath('text()').re('-\s([^\n]*?)\\n')
#            items.append(item)

        return items
