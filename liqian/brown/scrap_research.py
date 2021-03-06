#!/usr/bin/python
#coding=utf-8
import urllib2
import HTMLParser
import sys
import xml.dom.minidom as minidom
from htmlentitydefs import entitydefs
import glob

reload(sys)
sys.setdefaultencoding('utf-8')
class MyParser(HTMLParser.HTMLParser):
	def __init__(self):
		HTMLParser.HTMLParser.__init__(self)
		self.hasname = False
		self.hastitle = False
		self.startmark = False
		self.namelist = []
		self.titlelist = []
		self.tempname = []
		self.temptitle = []

	def handle_starttag(self, tag, attrs):
		if tag == 'div':
			for name, value in attrs:
				if name == 'id' and value == 'content':
					self.startmark = True
		if self.startmark == True:
			if tag == 'h2':
				self.hastitle = True
			if tag == 'a' and self.hastitle == True:
				self.hasname = True
			
	def handle_data(self, text):
		if self.hasname and text.isspace() == False:
			self.tempname.append(text)
		if self.hastitle and text.isspace() == False:
			self.temptitle.append(text)

	def handle_endtag(self, tag):
		if tag == 'div' and self.startmark == True:
			self.startmark = False
		if tag == 'a':
			if self.hasname:
				self.hasname = False
		if tag == 'p':
			if self.hastitle:
				self.titlelist.append(self.temptitle)
				self.hastitle = False
				self.temptitle = []
				self.namelist.append(self.tempname)
				self.tempname = []

			

fout_xml = file('brown_research.xml', 'w')
doc = minidom.Document()
institution = doc.createElement("institution")
doc.appendChild(institution)

if True:
	rootUrl = 'http://cs.brown.edu/research/areas.html'
	response = urllib2.urlopen(rootUrl)
	html = response.read()
	my = MyParser()
	my.feed(html)
	for i in range(len(my.titlelist)):
		research = doc.createElement("research")
		institution.appendChild(research)
		groupname = doc.createElement("groupname")
		titlename = my.titlelist[i][0]
		print titlename
		namelist = my.namelist[i]
		groupname.appendChild(doc.createTextNode(titlename.encode('utf-8')))
		research.appendChild(groupname)

		for profname in namelist:
			namenode = doc.createElement("professorname")
			namenode.appendChild(doc.createTextNode(profname.encode('utf-8')))
			research.appendChild(namenode)

doc.writexml(fout_xml, "\t", "\t", "\n")
fout_xml.close()
