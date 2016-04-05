#!/usr/bin/python
#coding=utf-8
import urllib2
import HTMLParser
import sys
import xml.dom.minidom as minidom
from htmlentitydefs import entitydefs
import glob
import requests.packages.urllib3.util.ssl_
requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS = 'ALL'

reload(sys)
sys.setdefaultencoding('utf-8')

class MyParser(HTMLParser.HTMLParser):
	def __init__(self):
		HTMLParser.HTMLParser.__init__(self)
		self.hasname = False
		self.faketitle = False
		self.hastitle = False
		self.namelist = []
		self.titlelist = []
		self.tempname = []
		self.temptitle = []

	def handle_starttag(self, tag, attrs):
		if tag == 'td':
			for name, value in attrs:
				if name == 'bgcolor':
					if value == '#F8F8FB' or value == '#F0F0F4':
						self.hasname = True
		if tag == 'span':
			self.faketitle = True
		if self.faketitle == False and tag == 'strong':
			self.hastitle = True
			
	def handle_data(self, text):
		if self.hasname and text.isspace() == False:
			self.tempname.append(text)
			#print text
		if self.hastitle and text.isspace() == False:
			self.temptitle.append(text)
			#print text

	def handle_endtag(self, tag):
		if tag == 'a':
			if self.hasname:
				self.namelist.append(self.tempname)
				self.hasname = False
				self.tempname = []
				self.halfname = False
		if tag == 'strong':
			if self.hastitle:
				self.titlelist.append(self.temptitle)
				self.hastitle = False
				self.temptitle = []
			self.faketitle = False


fout_xml = file('UCI.xml', 'w')
doc = minidom.Document()
institution = doc.createElement("institution")
doc.appendChild(institution)

if True:
	rootUrl = 'http://www.cs.uci.edu/faculty/index.php'
	response = urllib2.urlopen(rootUrl)
	html = response.read()
	my = MyParser()
	my.feed(html)
	for i in range(len(my.namelist)):
		professor = doc.createElement("professor")

		name = my.namelist[i][0]
		titles = my.titlelist[i]

		namenode = doc.createElement("name")
		namenode.appendChild(doc.createTextNode(name))
		professor.appendChild(namenode)

		for title in titles:
			titlenode = doc.createElement("title")
			titlenode.appendChild(doc.createTextNode(title))
			professor.appendChild(titlenode)

		institution.appendChild(professor)

doc.writexml(fout_xml, "\t", "\t", "\n")
fout_xml.close()