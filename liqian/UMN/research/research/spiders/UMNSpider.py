import scrapy
import re
from research.items import ResearchItem
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class CaltechSpider(scrapy.Spider):
	name = "UMN"
	allowed_domains = ["cs.umn.edu"]
	start_urls = ["https://www.cs.umn.edu/research/research_areas"]

	def parse(self, response):
		item = ResearchItem()
		item['proflist'] = []
		# sel = response.xpath('//div[@id="interior_main_content"]/div[@class="adjust_right_margin"]')
		# item['groupname'] = response.xpath('//h1/text()').extract()[0]
		# for sel2 in sel.xpath('.//p/a/text()'):
		# 	tmpname = sel2.extract()
		# 	print tmpname
		# 	item['proflist'].append(tmpname)
		for sel in response.xpath('//div[@class="view-content"]/div'):
			item['groupname'] = sel.xpath('./div[@class="views-field views-field-title"]/h3/a/text()').extract()[0]
			item['proflist'] = []
			for sel2 in sel.xpath('./div[@class="views-field views-field-field-faculty"]/em/a/text()'):
				tmpname = sel2.extract()
				print tmpname
				item['proflist'].append(tmpname)

			yield item
