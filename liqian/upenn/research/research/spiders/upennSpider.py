import scrapy
from scrapy.http import FormRequest
import re
from research.items import ResearchItem
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
postname = "abc"
class CaltechSpider(scrapy.Spider):
	name = "upenn"
	allowed_domains = ["seas.upenn.edu"]
	start_urls = ["http://www.seas.upenn.edu/directory/departments.php"]

	def parse(self, response):
		for opt in response.xpath('//select[@name="centers"]/option/@value'):
			tmpname = opt.extract()
			postname = tmpname
	 		yield FormRequest.from_response(response, formxpath="//form[@method='post']", formdata={'departments':'Computer and Information Science (CIS)', 'centers': tmpname}, clickdata={'value': 'Go'}, callback=self.parse_page)
	
	def parse_page(self, response):
		#print response.xpath('//h2//text()').extract()[1]
		item = ResearchItem()
		item['proflist'] = []
		tmpname = response.xpath('//h2//text()').extract()
		item['groupname'] = tmpname[1]
		print str(item['groupname'])
		
		for sel in response.xpath('//table//table[@width="600"][@border="0"]'):
			for sel2 in sel.xpath('.//td'):
				title = sel2.xpath('strong/text()').extract()
				#print title
				if len(title) < 1:
					continue
				if title[0] == 'Name: ':
					sel3 = sel2.xpath('.//text()')
					tmpname = sel3.extract()[1][:-3]
					#print tmpname
					item['proflist'].append(tmpname)
		yield item