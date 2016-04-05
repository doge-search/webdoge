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
		self.hasemail = False
		self.hasphone = False
		self.hasoffice = False
		self.faketag = False
		self.endmark = False
		self.namelist = []
		self.titlelist = []
		self.phonelist = []
		self.emaillist = []
		self.officelist = []
		self.tempname = []
		self.temptitle = []
		self.tempphone = []
		self.tempemail = []
		self.tempoffice = []

	def handle_starttag(self, tag, attrs):
		if tag == 'li':
			for name, value in attrs:
				if name == 'class':
					if value == 'profile-name':
						self.hasname = True
					if value == 'profile-title':
						self.hastitle = True
			
	def handle_data(self, text):
		if self.hasname and text.isspace() == False:
			self.tempname.append(text)
		if self.hastitle and text.isspace() == False:
			self.temptitle.append(text)

	def handle_endtag(self, tag):
		if tag == 'li':
			if self.hasname:
				self.namelist.append(self.tempname)
				self.hasname = False
				self.tempname = []
			if self.hastitle:
				self.titlelist.append(self.temptitle)
				self.hastitle = False
				self.temptitle = []

			

fout_xml = file('brown.xml', 'w')
doc = minidom.Document()
institution = doc.createElement("institution")
doc.appendChild(institution)

if True:
	rootUrl = 'http://cs.brown.edu/people/faculty/'
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
