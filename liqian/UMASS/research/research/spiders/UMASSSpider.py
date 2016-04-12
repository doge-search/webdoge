import scrapy
import re
from research.items import ResearchItem
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class CaltechSpider(scrapy.Spider):
	name = "UMASS"
	allowed_domains = ["cics.umass.edu"]
	start_urls = ["https://www.cics.umass.edu/research/research-groups"]

	def parse(self, response):
		item = ResearchItem()
		for sel in response.xpath('//div[@class="view-content"]/div'):
			tempname = sel.xpath('.//div/h3/a/text()').extract()
			if not tempname:
				continue
			item['groupname'] = tempname[0]
			print str(item['groupname'])
			item['proflist'] = []
			for sel2 in sel.xpath('.//div[@class="views-field views-field-view"]//span[@class="views-field views-field-view-node"]/span/a/text()'):
				tmpname = sel2.extract()
				print tmpname
				item['proflist'].append(tmpname)
			
			yield item
