from scrapy.spiders import CrawlSpider,Rule
from scrapy.linkextractors.sgml import SgmlLinkExtractor
import re
from scrapy.http import Request
from scrapy.selector import HtmlXPathSelector
from profetch.items import proItem

class UIUCSpider(CrawlSpider):
    name = "UIUC"
    allowed_domains = ["cs.illinois.edu"]
    start_urls=["https://cs.illinois.edu/directory/faculty?quicktabs_faculty_tabs_new=0"]
    rules = (Rule(SgmlLinkExtractor(allow=('/directory/profile/\w*')),  callback = 'parse_pro', follow=True),)
    def parse_pro(self, response):
        theItem = proItem()
        sel = HtmlXPathSelector(response)
        print '!'
        # for person in sel.xpath('//div[@class="extDirectoryPerson"]'):
        #     print '!'
        #     continue
        #     theItem['website'] = ''
        #     theItem['email'] = ''
        #     theItem['title'] = ''
        #     theItem['phone'] = ''
        #     theItem['office'] = ''
        #     theItem['picture'] = ''
        #     picture = person.xpath('./div[@class="extDirectoryPhoto"]/a/img/@src').extract()
        #     if(len(picture) > 0):
        #         theItem['picture'] = picture[0]
        #     title = person.xpath('./div[@class="extDirectoryRole"]/div[@class="extDirectoryTitle"]').extract()
        #     if(len(title) > 0):
        #         theItem['title'] = title[0]
        #     website = person.xpath('./div[@class="extDirectoryRole"]/div[@class="extDirectoryEmail"]').extract()
        #     if(len(website) > 0):
        #         theItem['website'] = website[0]
        #     name = person.xpath('./div[@class="extDirectoryRole"]/div[@class="extDirectoryName"]').extract()
        #     if(len(name) > 0):
        #         theItem['name'] = name[0]
        #     office = person.xpath('./div[@class="extDirectoryRole"]/div[@class="extDirectoryOffice"]').extract()
        #     if(len(office) > 0):
        #         theItem['office'] = office[0]
        #     phone = person.xpath('./div[@class="extDirectoryRole"]/div[@class="extDirectoryPhone"]').extract()
        #     if(len(phone) > 0):
        #         theItem['phone'] = phone[0]
        #     email = person.xpath('./div[@class="extDirectoryRole"]/div[@class="extDirectoryEmail"]').extract()
        #     if(len(email) > 0):
        #         theItem['email'] = email[0]
        #
        #     # theItem['email'] = email
        #     # theItem['phone'] = span.xpath('./text()').extract()[1]
        #     # theItem['office'] = span.xpath('./text()').extract()[1]
        #     print theItem
        #     yield theItem
