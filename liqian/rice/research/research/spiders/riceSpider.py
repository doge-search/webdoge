import scrapy
import re
from research.items import ResearchItem
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class CaltechSpider(scrapy.Spider):
	name = "rice"
	allowed_domains = ["cs.rice.edu"]
	start_urls = ["https://www.cs.rice.edu/research/aai/", "https://www.cs.rice.edu/research/ces/", "https://www.cs.rice.edu/research/plse/"]

	def parse(self, response):
		item = ResearchItem()
		item['proflist'] = []
		tmpname = response.xpath('//div[@id="ctl00_ContentPlaceHolder1_MainContentBlock"]/h1/text()').extract()
		item['groupname'] = tmpname[0]
		print str(item['groupname'])
		sel = response.xpath('//table[@dropzone="copy"]')
		for sel2 in sel.xpath('.//td[@style="cursor: default; text-align: left; vertical-align: top;"]/p/a'):
			tmpname = sel2.xpath('text()').extract()
			print str(tmpname)
			item['proflist'].append(tmpname)

		yield item
