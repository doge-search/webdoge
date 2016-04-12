import scrapy
import re
from research.items import ResearchItem
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class CaltechSpider(scrapy.Spider):
	name = "UMD"
	allowed_domains = ["cs.umd.edu"]
	start_urls = ["http://www.cs.umd.edu/researcharea"]

	def parse(self, response):
		for href in response.xpath('//h4[@class="field-content"]/a/@href'):
			url = response.urljoin(href.extract())
			yield scrapy.Request(url, callback=self.parse_page)
	
	def parse_page(self, response):
		item = ResearchItem()
		item['proflist'] = []
		tmpname = response.xpath('//h1[@class="title"][@id="page-title"]/text()').extract()
		item['groupname'] = tmpname[0]
		print str(item['groupname'])
		for sel in response.xpath('//div[@class="views-field views-field-field-person-last-name"]/div/a'):
			tmpname = sel.xpath('text()').extract()
			print str(tmpname)
			item['proflist'].append(tmpname)
			
		yield item
