import scrapy
import re
from research.items import ResearchItem
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class CaltechSpider(scrapy.Spider):
	name = "duke"
	allowed_domains = ["cs.duke.edu"]
	start_urls = ["http://www.cs.duke.edu/research/"]

	def parse(self, response):
		for href in response.xpath('//div[@id="ResearchGroupsLinks"]//div/a/@href'):
			url = response.urljoin(href.extract())
			yield scrapy.Request(url, callback=self.parse_page)
	
	def parse_page(self, response):
		item = ResearchItem()
		item['proflist'] = []
		tmpname = response.xpath('//p[@id="ResearchPageTitle"]/text()').extract()
		item['groupname'] = tmpname[0]
		print str(item['groupname'])
		for sel in response.xpath('//div[@id="ResearchRightColumn"]//li/a'):
			tmpname = sel.xpath('text()').extract()
			print str(tmpname)
			item['proflist'].append(tmpname)
			
		yield item
