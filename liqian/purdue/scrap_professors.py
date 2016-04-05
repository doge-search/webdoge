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
		self.enter = False
		self.count = 0
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
		if tag == 'tr':
			self.enter = True
		if self.enter == True and tag == 'td':
			self.count += 1
			
	def handle_data(self, text):
		if self.count == 1 and text.isspace() == False:
			self.tempname.append(text)
		if self.count == 2 and text.isspace() == False:
			self.temptitle.append(text)
		if self.count == 3 and text.isspace() == False:
			self.tempphone.append(text)
		if self.count == 4 and text.isspace() == False:
			self.tempoffice.append(text)

	def handle_endtag(self, tag):
		if tag == 'tr' and self.count > 0:
			if self.tempname:
				self.namelist.append(self.tempname)
				self.hasname = False
				self.tempname = []
			if self.temptitle:
				self.titlelist.append(self.temptitle)
				self.hastitle = False
				self.temptitle = []
			if self.tempphone:
				self.phonelist.append(self.tempphone)
				self.hasphone = False
			if self.tempoffice:
				self.officelist.append(self.tempoffice)
				self.hasoffice = False
			if not self.tempphone:
				self.tempphone.append('null')
				self.phonelist.append(self.tempphone)
			if not self.tempoffice:
				self.tempoffice.append('null')
				self.officelist.append(self.tempoffice)
					
			self.tempphone = []
			self.tempoffice = []
			self.count = 0

			

fout_xml = file('purdue.xml', 'w')
doc = minidom.Document()
institution = doc.createElement("institution")
doc.appendChild(institution)

if True:
	rootUrl = 'https://www.cs.purdue.edu/people/faculty/index.html'
	response = urllib2.urlopen(rootUrl)
	html = response.read()
	my = MyParser()
	my.feed(html)
	for i in range(len(my.namelist)):
		professor = doc.createElement("professor")

		name = my.namelist[i][0]
		titles = my.titlelist[i]
		phone = my.phonelist[i][0]
		office = my.officelist[i][0]

		namenode = doc.createElement("name")
		namenode.appendChild(doc.createTextNode(name))
		professor.appendChild(namenode)

		for title in titles:
			titlenode = doc.createElement("title")
			titlenode.appendChild(doc.createTextNode(title))
			professor.appendChild(titlenode)

		phonenode = doc.createElement("phone")
		phonenode.appendChild(doc.createTextNode(phone))
		professor.appendChild(phonenode)

		officenode = doc.createElement("office")
		officenode.appendChild(doc.createTextNode(office))
		professor.appendChild(officenode)

		institution.appendChild(professor)

doc.writexml(fout_xml, "\t", "\t", "\n")
fout_xml.close()#
