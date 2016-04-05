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
		self.namelist = []
		self.titlelist = []
		self.emaillist = []
		self.tempname = []
		self.temptitle = []
		self.tempemail = []

	def handle_starttag(self, tag, attrs):
		if tag == 'h2':
			for name, value in attrs:
				if name == 'class' and value == 'person-name':
					self.hasname = True
		if tag == 'li':
			for name, value in attrs:
				if name == 'class' and value == 'appointment':
					self.hastitle = True

		if tag == 'span':
			for name, value in attrs:
				if name == 'class' and value == 'km-email':
					self.hasemail = True
			
	def handle_data(self, text):
		if self.hasname and text.isspace() == False:
			self.tempname.append(text)
			#print text
		if self.hastitle and text.isspace() == False:
			self.temptitle.append(text)
			#print text
		if self.hasemail and text.isspace() == False:
			self.tempemail.append(text)
			print text

	def handle_endtag(self, tag):
		if tag == 'a':
			if self.hasname:
				self.namelist.append(self.tempname)
				self.hasname = False
				self.tempname = []
			# else:
			# 	self.namelist.append(['null'])
		if tag == 'ul':
			if self.hastitle:
				self.titlelist.append(self.temptitle)
				self.hastitle = False
				self.temptitle = []
			# else:
			# 	self.titlelist.append(['null'])
		if tag == 'span':
			if self.hasemail:
				self.emaillist.append(self.tempemail)
				self.hasemail = False
				self.tempemail = []
			# else:
			# 	self.emaillist.append(['null'])

fout_xml = file('OSU.xml', 'w')
doc = minidom.Document()
institution = doc.createElement("institution")
doc.appendChild(institution)

if True:
	rootUrl = 'https://cse.osu.edu/about-us/faculty'
	response = urllib2.urlopen(rootUrl)
	html = response.read()
	my = MyParser()
	my.feed(my.unescape(html))
	for i in range(len(my.namelist)):
		professor = doc.createElement("professor")

		name = my.namelist[i][0]
		titles = my.titlelist[i]
		email = my.emaillist[i][0]

		namenode = doc.createElement("name")
		namenode.appendChild(doc.createTextNode(name))
		professor.appendChild(namenode)

		for title in titles:
			titlenode = doc.createElement("title")
			titlenode.appendChild(doc.createTextNode(title))
			professor.appendChild(titlenode)

		emailnode = doc.createElement("email")
		emailnode.appendChild(doc.createTextNode(email))
		professor.appendChild(emailnode)

		institution.appendChild(professor)

doc.writexml(fout_xml, "\t", "\t", "\n")
fout_xml.close()