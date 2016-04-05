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
		self.enter = False
		self.namelist = []
	def handle_starttag(self, tag, attrs):
		if tag == 'td':
			for name, value in attrs:
				if name == 'rowspan':
					if value == '7':
						self.enter = True
		if tag == 'a' and self.hasname == True:
			self.hasname = False
	def handle_data(self, text):
		if self.hasname and text.isspace() == False:
			self.namelist.append(text[:-3])
		if self.enter and text.isspace() == False:
			if text == 'Name: ':
				self.hasname = True
	def handle_charref(self, ref):
		self.handle_entityref("#" + ref)
	def handle_entityref(self, ref):
		self.handle_data(self.unescape("&%s;" % ref))
	def handle_endtag(self, tag):
		if tag == 'tr' and self.enter == True:
			self.enter = False

fout_xml = file('upenn.xml', 'w')
doc = minidom.Document()
institution = doc.createElement("institution")
doc.appendChild(institution)

if True:
	rootUrl = 'http://www.seas.upenn.edu/directory/departments.php?adv=yes&departments=Computer%20and%20Information%20Science%20(CIS)&AdvSearch=yes'
	response = urllib2.urlopen(rootUrl)
	html = response.read()
	html = unicode(html, errors='ignore')
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


