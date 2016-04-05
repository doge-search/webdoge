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
		if tag == 'div':
			for name, value in attrs:
				if name == 'class':
					if value == 'field field-name-title field-type-ds field-label-hidden':
						self.hasname = True
					if value == 'field field-name-field-position field-type-text field-label-hidden':
						self.hastitle = True
					if value == 'field field-name-field-email field-type-email field-label-hidden':
						self.hasemail = True
						self.endmark = True
					if value == 'field field-name-field-phone field-type-text field-label-inline clearfix':
						self.hasphone = True
					if value == 'field field-name-field-location field-type-text field-label-inline clearfix':
						self.hasoffice = True
					if value == 'field-label':
						self.faketag = True
			
	def handle_data(self, text):
		if self.faketag == False:
			if self.hasname and text.isspace() == False:
				self.tempname.append(text)
			if self.hastitle and text.isspace() == False:
				self.temptitle.append(text)
			if self.hasemail and text.isspace() == False:
				self.tempemail.append(text)
			if self.hasphone and text.isspace() == False:
				self.tempphone.append(text)
			if self.hasoffice and text.isspace() == False:
				self.tempoffice.append(text)

	def handle_endtag(self, tag):
		if tag == 'div' and self.faketag == True:
			self.faketag = False
			return
		if tag == 'div':
			if self.hasname:
				self.namelist.append(self.tempname)
				self.hasname = False
				self.tempname = []
			if self.hastitle:
				self.titlelist.append(self.temptitle)
				self.hastitle = False
				self.temptitle = []
			if self.hasemail:
				if not self.tempemail:
					self.tempemail.append('null')
				self.emaillist.append(self.tempemail)
				self.hasemail = False
			if self.hasphone:
				if not self.tempphone:
					self.tempphone.append('null')
				self.phonelist.append(self.tempphone)
				self.hasphone = False
			if self.hasoffice:
				if not self.tempoffice:
					self.tempoffice.append('null')
				self.officelist.append(self.tempoffice)
				self.hasoffice = False
			if self.endmark:
				if not self.tempphone:
					self.tempphone.append('null')
					self.phonelist.append(self.tempphone)
				if not self.tempemail:
					self.tempemail.append('null')
					self.emaillist.append(self.tempemail)
				if not self.tempoffice:
					self.tempoffice.append('null')
					self.officelist.append(self.tempoffice)
					
				self.tempphone = []
				self.tempemail = []
				self.tempoffice = []
				self.endmark = False

			

fout_xml = file('UMASS.xml', 'w')
doc = minidom.Document()
institution = doc.createElement("institution")
doc.appendChild(institution)

if True:
	rootUrl = 'https://www.cics.umass.edu/faculty/faculty-directory'
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

		emailnode = doc.createElement("email")
		emailnode.appendChild(doc.createTextNode(email))
		professor.appendChild(emailnode)

		institution.appendChild(professor)

doc.writexml(fout_xml, "\t", "\t", "\n")
fout_xml.close()

