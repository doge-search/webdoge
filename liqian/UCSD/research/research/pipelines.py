# -- coding: utf-8 --

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os
import urllib
import xml.dom.minidom as minidom

class xmlPipeline(object):
	def __init__(self):
		self.fout_xml = file('../UCSD_research.xml', 'w')
		self.doc = minidom.Document()
		self.institution = self.doc.createElement("institution")
		self.doc.appendChild(self.institution)
		self.cnt = 0

	def process_item(self, item, spider):
		research = self.doc.createElement("research")
		self.institution.appendChild(research)
		groupname = self.doc.createElement("groupname")
		groupname.appendChild(self.doc.createTextNode(item['groupname'].encode('utf-8')))
		research.appendChild(groupname)

		for profname in item['proflist']:
			namenode = self.doc.createElement("professorname")
			namenode.appendChild(self.doc.createTextNode(profname))
			research.appendChild(namenode)
		self.cnt += 1

	def close_spider(self, spider):
		print self.cnt
		self.doc.writexml(self.fout_xml, "\t", "\t", "\n", encoding="utf-8")
		self.fout_xml.close()
