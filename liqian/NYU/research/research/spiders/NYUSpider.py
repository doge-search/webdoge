import scrapy
import re
from research.items import ResearchItem
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class CaltechSpider(scrapy.Spider):
	name = "NYU"
	allowed_domains = ["cs.nyu.edu"]
	start_urls = ["https://cs.nyu.edu/dynamic/research/areas/"]

	def parse(self, response):
		item = ResearchItem()
		item['proflist'] = []

		for sel in response.xpath('//div[@class="inner areas"]/div'):
			item['groupname'] = sel.xpath('h2/text()').extract()[0]
			item['proflist'] = []
			for sel3 in sel.xpath('.//div[@class="row faculty"]/div/p/a/text()'):
				tmpname = sel3.extract()
				print tmpname
				item['proflist'].append(tmpname)
			
			yield item
