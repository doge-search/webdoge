import scrapy
import re
from research.items import ResearchItem
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class CaltechSpider(scrapy.Spider):
	name = "PSU"
	allowed_domains = ["eecs.psu.edu"]
	start_urls = [
		"http://www.eecs.psu.edu/research/Facilities/EECS-Research-Labs-Communications-Networking.aspx",
		"http://www.eecs.psu.edu/research/Facilities/EECS-Research-Facilities-Labs-Computational-Biology-and-Biomedicine-Area.aspx",
		"http://www.eecs.psu.edu/research/Facilities/EECS-Research-Labs-Control-Systems.aspx",
		"http://www.eecs.psu.edu/research/Facilities/EECS-Research-Labs-Cyber-Security.aspx",
		"http://www.eecs.psu.edu/research/Facilities/EECS-Research-Facilities-Labs-iPDA.aspx",
		"http://www.eecs.psu.edu/research/Facilities/EECS-Research-Facilities-Labs-TCS.aspx"		
	]

	def parse(self, response):
		item = ResearchItem()
		item['proflist'] = []
		sel = response.xpath('//div[@id="interior_main_content"]/div[@class="adjust_right_margin"]')
		item['groupname'] = response.xpath('//h1/text()').extract()[0]
		for sel2 in sel.xpath('.//p/a/text()'):
			tmpname = sel2.extract()
			print tmpname
			item['proflist'].append(tmpname)
			
		yield item
