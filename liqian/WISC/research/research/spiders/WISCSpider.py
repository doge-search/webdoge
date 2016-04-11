import scrapy
import re
from research.items import ResearchItem
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class CaltechSpider(scrapy.Spider):
	name = "WISC"
	allowed_domains = ["cs.wisc.edu"]
	start_urls = ["https://www.cs.wisc.edu/research/groups"]

	def parse(self, response):
		item = ResearchItem()
		for sel in response.xpath('//table[@class="views-table cols-2"]'):
			item['groupname'] = sel.xpath('caption/text()').extract()[0]
			item['proflist'] = []
			for selp in sel.xpath('.//div[@class="views-field views-field-name-1"]/span/a'):
				tmpname = selp.xpath('text()').extract()
				print str(tmpname)
				item['proflist'].append(tmpname)
			yield item
