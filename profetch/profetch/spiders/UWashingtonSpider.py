from scrapy.spiders import CrawlSpider,Rule
from scrapy.linkextractors.sgml import SgmlLinkExtractor
import re
from scrapy.http import Request
from scrapy.selector import HtmlXPathSelector
from profetch.items import proItem

class UWashingtonSpider(CrawlSpider):
    name = "UW"
    allowed_domains = ["www.cs.washington.edu"]
    start_urls=["https://www.cs.washington.edu/people/faculty"]
    rules = (Rule(SgmlLinkExtractor(allow=('/people/faculty/\w*')),  callback = 'parse_pro', follow=True),)
    def parse_pro(self, response):
        theItem = proItem()
        sel = HtmlXPathSelector(response)
        theItem['name'] = ''
        theItem['website'] = ''
        theItem['email'] = ''
        theItem['title'] = ''
        theItem['phone'] = ''
        theItem['office'] = ''
        theItem['picture'] = ''
        content = sel.xpath('//div[@class="node node-page view-mode-full clearfix"]/span/@content')
        name = content.extract()
        if(len(name) > 0):
            theItem['name'] = name[0]
        content = sel.xpath('//div[@class="block block-block first last odd"]/div[@class="content"]')
        picture = content.xpath('./img[@width="160"]/@src').extract()
        if(len(picture) > 0):
            url = picture[0]
            if(url[0]=='/'):
                url = 'https://www.cs.washington.edu' + url
            theItem['picture'] = url
        for p in content.xpath('.//p'):
            msglst = p.xpath('./text()').extract()
            if(len(msglst) == 0):
                continue
            msg = msglst[0]
            if(msg[0:3]=='Off'):
                theItem['office'] = msg[8:]
            if(msg[0:3]=='Ema'):
                theItem['email'] = msg[7:]
            if(msg[0:3]=='Phone'):
                theItem['phone'] = msg[7:]

        yield theItem
