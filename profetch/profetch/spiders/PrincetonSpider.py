from scrapy.spiders import CrawlSpider,Rule
from scrapy.linkextractors.sgml import SgmlLinkExtractor
import re
from scrapy.http import Request
from scrapy.selector import HtmlXPathSelector

from profetch.items import proItem


class PrincetonSpider(CrawlSpider):
    name = "Princeton"
    allowed_domains = ["www.cs.princeton.edu"]
    start_urls=["https://www.cs.princeton.edu/people/faculty"]
    rules = (Rule(SgmlLinkExtractor(allow=('/people/profile/\w*')),  callback = 'parse_pro', follow=True),)
    def parse_pro(self, response):
        theItem = proItem()
        sel = HtmlXPathSelector(response)
        theItem['name'] = sel.xpath('//h1[@class="page-header"]/text()').extract()[0]
        theItem['website'] = ''
        theItem['email'] = ''
        theItem['phone'] = ''
        theItem['office'] = ''
        theItem['picture'] = ''
        basic = sel.xpath('//div[@class="faculty-bio-basics"]')
        pic = sel.xpath('//div[@class="faculty-bio-picture"]')
        img_lst = pic.xpath('.//img/@src').extract()
        if(len(img_lst) > 0):
            theItem['picture'] = "https://www.cs.princeton.edu" + img_lst[0]

        for row in basic.xpath('div[@class="faculty-bio-row"]'):
            label = row.xpath('div[@class="faculty-bio-label"]/text()').extract()
            if(len(label) > 0 and 'Homepage' in label[0]):
                website = row.xpath('div[@class="faculty-bio-value"]/a/text()').extract()[0]
                theItem['website'] = website
            if(len(label)==0):
                spans = row.xpath('div[@class="faculty-bio-value"]//span[@class="person-address-item"]')
                if(len(spans)==3):
                    cnt = 0
                    for span in spans:
                        cnt += 1
                        # print span.xpath('./text()').extract()[1]
                        if(cnt==1):
                            email = span.xpath('./text()').extract()[1]
                            theItem['email'] = email
                        if(cnt==2):
                            theItem['phone'] = span.xpath('./text()').extract()[1]
                        if(cnt==3):
                            theItem['office'] = span.xpath('./text()').extract()[1]
                # print email

        yield theItem
