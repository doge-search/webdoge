import scrapy
import re
from research.items import ResearchItem
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class CaltechSpider(scrapy.Spider):
	name = "Caltech"
	allowed_domains = ["cms.caltech.edu"]
	start_urls = ["http://www.cms.caltech.edu/research"]

	def parse(self, response):
		for href in response.xpath('//ul[@class="listing small"]/li/a/@href'):
			url = response.urljoin(href.extract())
			yield scrapy.Request(url, callback=self.parse_page)
	
	def parse_page(self, response):
		item = ResearchItem()
		item['proflist'] = []
		tmpname = response.xpath('//div[@class="content-holder"]/h1/text()').extract()
		item['groupname'] = tmpname[0].split('>')[1][1:]
		print str(item['groupname'])
		for sel in response.xpath('//div[@class="aside-faculty"]//a'):
			tmpname = sel.xpath('text()').extract()
			print str(tmpname)
			item['proflist'].append(tmpname)
			

		yield item
