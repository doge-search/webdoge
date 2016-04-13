import scrapy
import re
from research.items import ResearchItem
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class CaltechSpider(scrapy.Spider):
	name = "OSU"
	allowed_domains = ["cse.osu.edu"]
	start_urls = [
		"https://cse.osu.edu/research/artificial-intelligence",
		"https://cse.osu.edu/research/computer-graphics",
		"https://cse.osu.edu/research/networking-distributed-computing",
		"https://cse.osu.edu/research/software-engineering-programming-languages",
		"https://cse.osu.edu/research/systems",
		"https://cse.osu.edu/research/theory-algorithms"
	]

	def parse(self, response):
		item = ResearchItem()
		item['proflist'] = []
		sel = response.xpath('//ul[@class="osu-people-directory"]')
		item['groupname'] = response.xpath('//div[@class="panel-title-pane"]/h1/text()').extract()[0]
		for sel2 in sel.xpath('.//h2[@class="person-name"]/a/text()'):
			tmpname = sel2.extract()
			print tmpname
			item['proflist'].append(tmpname)
			
		yield item
