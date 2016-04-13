import scrapy
import re
from research.items import ResearchItem
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class CaltechSpider(scrapy.Spider):
	name = "UCI"
	allowed_domains = ["ics.uci.edu"]
	start_urls = ["http://www.ics.uci.edu//faculty/area/"]

	def parse(self, response):
		rooturl = "http://www.ics.uci.edu//faculty/area/"
		for href in response.xpath('//div[@id="content_text"]/p/a/@href'):
			url = rooturl + href.extract()
			print url
			yield scrapy.Request(url, callback=self.parse_page)
	
	def parse_page(self, response):
		item = ResearchItem()
		item['proflist'] = []
		tmpname = response.xpath('//div[@id="content_title"]/text()').extract()
		item['groupname'] = tmpname[0]
		print str(item['groupname'])
		for sel in response.xpath('//div[@id="content_text"]//a'):
			tmpname = sel.xpath('text()').extract()
			print str(tmpname)
			item['proflist'].append(tmpname)
			
		yield item
