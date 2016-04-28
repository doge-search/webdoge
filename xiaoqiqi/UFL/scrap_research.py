#coding=utf-8
#!~/python2.7.10/bin/python

import urllib
import urllib2
import re
import os
import sys
from bs4 import BeautifulSoup
import xml.dom.minidom as minidom
import time
import socket

reload(sys) 
sys.setdefaultencoding('utf-8')

fout_xml = file('UFL_research.xml', 'w')
doc = minidom.Document()
institution = doc.createElement("institution")
doc.appendChild(institution)

if __name__ == '__main__':
	url = 'https://www.cise.ufl.edu/ciseresearch/algorithms'
	html = urllib2.urlopen(url).read()
	soup = BeautifulSoup(html)
	content = soup.find('li',{'class':'first expanded active-trail menu-mlid-346'})
	areaList = content.findAll('li')
	for i in range(len(areaList)):
		research = doc.createElement("research")
		grouptext = areaList[i].find("a").text
		groupname = doc.createElement("groupname")
		groupname.appendChild(doc.createTextNode(grouptext))
		research.appendChild(groupname)
		groupurl = 'https://www.cise.ufl.edu/'+areaList[i].find('a')['href']
		grouphtml = urllib2.urlopen(groupurl).read()
		groupsoup = BeautifulSoup(grouphtml)
		prof = groupsoup.find('div',{'id':'content-body'})
		professor = prof.findAll('div',{'class':'views-field views-field-field-fuul-name'})
		for p in professor:
			professorname = doc.createElement("professorname")
			professorname.appendChild(doc.createTextNode(p.text))
			research.appendChild(professorname)
		institution.appendChild(research)
	doc.writexml(fout_xml, "\t", "\t", "\n")
	fout_xml.close()
	
		