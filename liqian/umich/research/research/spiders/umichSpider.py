import scrapy
import re
from research.items import ResearchItem
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class CaltechSpider(scrapy.Spider):
	name = "umich"
	allowed_domains = ["eecs.umich.edu"]
	start_urls = ["http://www.eecs.umich.edu/eecs/research/cseareas.html"]

	def parse(self, response):
		rooturl = 'http://www.eecs.umich.edu/eecs/research/'
		for href in response.xpath('//td[@align="left"][@valign="top"]/a[@class="alpha"]/@href'):
			url = rooturl + href.extract()
	 		yield scrapy.Request(url, callback=self.parse_page)
	
	def parse_page(self, response):
		item = ResearchItem()
		item['proflist'] = []
		tmpname = response.xpath('//td[@colspan="3"][@height="30"]/h1/text()').extract()
		item['groupname'] = tmpname[0]
		print str(item['groupname'])
		sel = response.xpath('//td[@style="border-left:1px solid #333;"]')
		print sel
		sel2 = sel.xpath('ul[1]')
		for sel3 in sel2.xpath('li/a'):
			tmpname = sel3.xpath('text()').extract()
			print str(tmpname)
			item['proflist'].append(tmpname)

		yield item
