import scrapy
import re
from research.items import ResearchItem
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class CaltechSpider(scrapy.Spider):
	name = "harvard"
	allowed_domains = ["seas.harvard.edu"]
	start_urls = ["http://www.seas.harvard.edu/faculty-research/research"]

	def parse(self, response):
		item = ResearchItem()
		item['proflist'] = []
		sel = response.xpath('//div[@class="view-grouping-header"]/a[@href="/computer-science"]')
		sel = sel.xpath('..')
		sel = sel.xpath('..')

		for sel2 in sel.xpath('div[@class="view-grouping-content"]/div[@class="item-list"]'):
			item['groupname'] = sel2.xpath('h3/text()').extract()[0]
			item['proflist'] = []
			for sel3 in sel2.xpath('.//div[@class="views-field views-field-view-node"]/span/a/text()'):
				tmpname = sel3.extract()
				print tmpname
				item['proflist'].append(tmpname)
			
			yield item
