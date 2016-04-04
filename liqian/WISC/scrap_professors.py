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
		self.namelist = []
		self.titlelist = []
		self.phonelist = []
		self.emaillist = []
		self.tempname = []
		self.temptitle = []
		self.tempphone = []
		self.tempemail = []

	def handle_starttag(self, tag, attrs):
		if tag == 'div':
			for name, value in attrs:
				if name == 'class':
					if value == 'views-field views-field-field-full-name':
						self.hasname = True
					if value == 'views-field views-field-field-title':
						self.hastitle = True
					if value == 'views-field views-field-mail':
						self.hasemail = True
					if value == 'views-field views-field-field-office-phone':
						self.hasphone = True
			
	def handle_data(self, text):
		if self.hasname and text.isspace() == False:
			self.tempname.append(text)
		if self.hastitle and text.isspace() == False:
			self.temptitle.append(text)
		if self.hasemail and text.isspace() == False:
			self.tempemail.append(text)
		if self.hasphone and text.isspace() == False:
			self.tempphone.append(text)

	def handle_endtag(self, tag):
		if tag == 'div':
			if self.hasname:
				self.namelist.append(self.tempname)
				self.hasname = False
				self.tempname = []
			# else:
			# 	self.namelist.append(['null'])
			if self.hastitle:
				self.titlelist.append(self.temptitle)
				self.hastitle = False
				self.temptitle = []
			# else:
			# 	self.titlelist.append(['null'])
			if self.hasemail:
				self.emaillist.append(self.tempemail)
				self.hasemail = False
				self.tempemail = []
			# else:
			# 	self.emaillist.append(['null'])
			if self.hasphone:
				if not self.tempphone:
					self.tempphone.append('null')
				self.phonelist.append(self.tempphone)
				self.hasphone = False
				self.tempphone = []
			# else:
			# 	self.phonelist.append(['null'])

fout_xml = file('WISC.xml', 'w')
doc = minidom.Document()
institution = doc.createElement("institution")
doc.appendChild(institution)

if True:
	rootUrl = 'https://www.cs.wisc.edu/people/faculty'
	response = urllib2.urlopen(rootUrl)
	html = response.read()
	my = MyParser()
	my.feed(html)
	for i in range(len(my.namelist)):
		professor = doc.createElement("professor")

		name = my.namelist[i][0]
		titles = my.titlelist[i]
		phone = my.phonelist[i][0]
		email = my.emaillist[i][0]

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

		emailnode = doc.createElement("email")
		emailnode.appendChild(doc.createTextNode(email))
		professor.appendChild(emailnode)

		institution.appendChild(professor)

doc.writexml(fout_xml, "\t", "\t", "\n")
fout_xml.close()