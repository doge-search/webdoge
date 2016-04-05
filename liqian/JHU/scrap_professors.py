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
		self.halfname = False
		self.hastitle = False
		self.namelist = []
		self.titlelist = []
		self.tempname = []
		self.temptitle = []

	def handle_starttag(self, tag, attrs):
		if tag == 'h3':
			self.halfname = True
		if tag == 'h6':
			self.hastitle = True
		if self.halfname == True and tag == 'a':
			for name, value in attrs:
				if name == 'style':
					if value == 'color:#5E6F7F;':
						self.hasname = True
					else:
						self.hasname = False
			
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
		if tag == 'h6':
			if self.hastitle:
				self.titlelist.append(self.temptitle)
				self.hastitle = False
				self.temptitle = []


fout_xml = file('JHU.xml', 'w')
doc = minidom.Document()
institution = doc.createElement("institution")
doc.appendChild(institution)

if True:
	rootUrl = 'http://www.cs.jhu.edu/faculty/'
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