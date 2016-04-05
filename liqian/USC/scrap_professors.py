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
escaped = '&lt;abc&gt;'

class MyParser(HTMLParser.HTMLParser):
	def __init__(self):
		HTMLParser.HTMLParser.__init__(self)
		self.hasname = False
		self.hastitle = False
		self.hasemail = False
		self.hasphone = False
		self.namelist = []
		self.titlelist = []
		self.phonelist = []
		self.emaillist = []
		self.tempname = []
		self.temptitle = []
		self.tempphone = []
		self.tempemail = []

	def handle_starttag(self, tag, attrs):
		if tag == 'td':
			for name, value in attrs:
				if name == 'class':
					if value == 'tdstyle2':
						self.hasname = True
			
	def handle_data(self, text):
		if self.hasname and text.isspace() == False:
			self.tempname.append(text)

	def handle_endtag(self, tag):
		if tag == 'a':
			if self.hasname:
				self.namelist.append(self.tempname)
				self.hasname = False
				self.tempname = []

fout_xml = file('USC.xml', 'w')
doc = minidom.Document()
institution = doc.createElement("institution")
doc.appendChild(institution)

if True:
	rootUrl = 'http://www.cs.usc.edu/faculty_staff/faculty/'
	response = urllib2.urlopen(rootUrl)
	html = response.read()
	my = MyParser()
	my.feed(html)
	for i in range(len(my.namelist)):
		professor = doc.createElement("professor")

		name = my.namelist[i][0]

		namenode = doc.createElement("name")
		namenode.appendChild(doc.createTextNode(name))
		professor.appendChild(namenode)

		institution.appendChild(professor)

doc.writexml(fout_xml, "\t", "\t", "\n")
fout_xml.close()