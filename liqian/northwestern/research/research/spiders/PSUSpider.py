import scrapy
import re
from research.items import ResearchItem
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class CaltechSpider(scrapy.Spider):
	name = "northwestern"
	allowed_domains = ["eecs.psu.edu"]
	start_urls = [
		"http://www.mccormick.northwestern.edu/eecs/computer-science/research/systems-networking.html",
		"http://www.mccormick.northwestern.edu/eecs/computer-science/research/theory.html",
		"http://www.mccormick.northwestern.edu/eecs/computer-science/research/artificial-intelligence-machine-learning.html",
		"http://www.mccormick.northwestern.edu/eecs/computer-science/research/human-computer-interaction.html",
		"http://www.mccormick.northwestern.edu/eecs/computer-science/research/graphics.html",
		"http://www.mccormick.northwestern.edu/eecs/computer-science/research/robotics.html",
	]

	def parse(self, response):
		item = ResearchItem()
		item['proflist'] = []
		sel = response.xpath('//div[@id="faculty-directory"]')
		item['groupname'] = response.xpath('//h1[@id="page-title"]/text()').extract()[0]
		for sel2 in sel.xpath('.//h3/a/text()'):
			tmpname = sel2.extract()
			print tmpname
			item['proflist'].append(tmpname)
			
		yield item
