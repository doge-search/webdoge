import scrapy
import re
from research.items import ResearchItem
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class CaltechSpider(scrapy.Spider):
	name = "purdue"
	allowed_domains = ["cs.purdue.edu"]
	start_urls = ["https://www.cs.purdue.edu/research/"]

	def parse(self, response):
		item = ResearchItem()
		for sel2 in response.xpath('//div[@class="panel panel-default area"]'):
			item['groupname'] = sel2.xpath('.//div[@class="panel-heading"]/h3/text()').extract()[0]
			print str(item['groupname'])
			item['proflist'] = []
			for sel3 in sel2.xpath('.//div[@class="panel-body"]/p/a/text()'):
				tmpname = sel3.extract()
				print tmpname
				item['proflist'].append(tmpname)
			
			yield item
