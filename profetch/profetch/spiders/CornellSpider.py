from scrapy.spiders import CrawlSpider,Rule
from scrapy.linkextractors.sgml import SgmlLinkExtractor
import re
from scrapy.http import Request
from scrapy.selector import HtmlXPathSelector
from profetch.items import proItem

class CornellSpider(CrawlSpider):
    name = "Cornell"
    allowed_domains = ["www.cs.cornell.edu"]
    start_urls=["https://www.cs.cornell.edu/people/faculty"]
    rules = (Rule(SgmlLinkExtractor(allow=('/people/faculty')),  callback = 'parse_main', follow=True),)
    def parse_main(self, response):
        theItem = proItem()
        sel = HtmlXPathSelector(response)
        for person in sel.xpath('//div[@class="person"]'):
            theItem['website'] = ''
            theItem['email'] = ''
            theItem['phone'] = ''
            theItem['office'] = ''
            theItem['picture'] = ''
            person.xpath('./a/@href').extract()
            website = person.xpath('./a/@href').extract()
            if(len(website) > 0):
                theItem['website'] = website[0]
            name = person.xpath('./a/img/@alt').extract()
            if(len(name) > 0):
                theItem['name'] = name[0]
            url = person.xpath('./a/img/@src').extract()
            if(len(url) > 0):
                theItem['picture'] = "https://www.cs.cornell.edu" + url[0]
            # theItem['email'] = email
            # theItem['phone'] = span.xpath('./text()').extract()[1]
            # theItem['office'] = span.xpath('./text()').extract()[1]
            print theItem
            yield theItem
