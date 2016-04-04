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
escaped = '&lt;abc&gt;'

class MyParser(HTMLParser.HTMLParser):
	def __init__(self):
		HTMLParser.HTMLParser.__init__(self)
		self.hasname = False
		self.namelist = []
	def handle_starttag(self, tag, attrs):
		if tag == 'td':
			for name, value in attrs:
				if name == 'valign':
					if value == 'top':
						self.hasname = True
	def handle_data(self, text):
		if self.hasname and text.isspace() == False:
			self.namelist.append(text)
	def handle_charref(self, ref):
		self.handle_entityref("#" + ref)
	def handle_entityref(self, ref):
		self.handle_data(self.unescape("&%s;" % ref))
	def handle_endtag(self, tag):
		if tag == 'a' and self.hasname == True:
			self.hasname = False

fout_xml = file('columbia.xml', 'w')
doc = minidom.Document()
institution = doc.createElement("institution")
doc.appendChild(institution)

if True:
	rootUrl = 'http://www.cs.columbia.edu/people/faculty'
	response = urllib2.urlopen(rootUrl)
	html = response.read()
	my = MyParser()
	my.feed(my.unescape(html))
	for i in range(len(my.namelist)):
		professor = doc.createElement("professor")
		name = my.namelist[i]
		namenode = doc.createElement("name")
		namenode.appendChild(doc.createTextNode(name))
		professor.appendChild(namenode)
		institution.appendChild(professor)

doc.writexml(fout_xml, "\t", "\t", "\n")
fout_xml.close()
