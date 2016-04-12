import scrapy
import re
from research.items import ResearchItem
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class CaltechSpider(scrapy.Spider):
	name = "JHU"
	allowed_domains = ["cs.jhu.edu"]
	start_urls = ["http://www.cs.jhu.edu/research/"]

	def parse(self, response):
		for href in response.xpath('//div[@class="submenu"]/ul[@class="sub-menu"]/li/a/@href'):
			url = href.extract()
	 		yield scrapy.Request(url, callback=self.parse_page)
	
	def parse_page(self, response):
		item = ResearchItem()
		item['proflist'] = []
		tmpname = response.xpath('//h1[@class="page-title"]/text()').extract()
		item['groupname'] = tmpname[0]
		print str(item['groupname'])

		for sel in response.xpath('//div[@class="the-content"]/p/a'):
			tmpname = sel.xpath('text()').extract()
			print str(tmpname)
			item['proflist'].append(tmpname)

		yield item
