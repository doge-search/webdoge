import scrapy
import re
from research.items import ResearchItem
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class CaltechSpider(scrapy.Spider):
	name = "USC"
	allowed_domains = ["cs.usc.edu"]
	start_urls = ["http://www.cs.usc.edu/research/research-areas-labs.htm"]

	def parse(self, response):
		item = ResearchItem()
		for sel in response.xpath('//div[@class="contentDetail"]/ul/li'):
			item['groupname'] = sel.xpath('a/text()').extract()[0]
			item['proflist'] = []
			for sel2 in sel.xpath('ul//li/i/text()'):
				tmplist = sel2.extract()
				print tmplist
				tmplist2 = tmplist.split('and')
				for names in tmplist2:
					namelist = names.split(',')
					for singlename in namelist:
						if singlename.strip() != '':
							item['proflist'].append(singlename)
						print singlename
			yield item
