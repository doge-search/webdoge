import scrapy
from scrapy.http import FormRequest
import re
from research.items import ResearchItem
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
postname = "abc"
class CaltechSpider(scrapy.Spider):
	name = "ucsd"
	allowed_domains = ["jacobsschool.ucsd.edu"]
	start_urls = ["http://jacobsschool.ucsd.edu/faculty/faculty_bios/findprofile.sfe?department=cse"]

	def parse(self, response):
		for opt in response.xpath('//select[@name="institute"]/option/@value'):
			tmpname = opt.extract()
			postname = tmpname
	 		yield FormRequest.from_response(response, formname='dirSearch', formdata={'institute': tmpname}, callback=self.parse_page)
	
	def parse_page(self, response):
		print postname
		# item = ResearchItem()
		# item['proflist'] = []
		# tmpname = response.xpath('//td[@colspan="3"][@height="30"]/h1/text()').extract()
		# item['groupname'] = tmpname[0]
		# print str(item['groupname'])
		# sel = response.xpath('//td[@style="border-left:1px solid #333;"]')
		# print sel
		# sel2 = sel.xpath('ul[1]')
		# for sel3 in sel2.xpath('li/a'):
		# 	tmpname = sel3.xpath('text()').extract()
		# 	print str(tmpname)
		# 	item['proflist'].append(tmpname)
		item = ResearchItem()
		item['groupname'] = postname
		item['proflist'] = []
		for sel in response.xpath('//p/a/text()'):
			tmpname = sel.extract()
			print tmpname
			item['proflist'].append(tmpname)

		yield item