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

fout_xml = file('MIT_research.xml', 'w')
doc = minidom.Document()
institution = doc.createElement("institution")
doc.appendChild(institution)

if __name__ == '__main__':
	url = 'http://www.eecs.mit.edu/people/faculty-advisors'
	html = urllib2.urlopen(url).read()
	soup = BeautifulSoup(html)
	content = soup.findAll('ul',{'class':'lab-theme-list'})
	areaList = content[2].findAll("li")
	for i in range(0,len(areaList)):
		research = doc.createElement("research")
		grouptext = areaList[i].text
		groupname = doc.createElement("groupname")
		groupname.appendChild(doc.createTextNode(grouptext))
		research.appendChild(groupname)
		groupurl = areaList[i].find("a")['href']
		grouphtml = urllib2.urlopen(groupurl).read()
		groupsoup = BeautifulSoup(grouphtml)
		people = groupsoup.find('div',{'class':'people-list'})
		professor = people.findAll("li")
		for p in professor:
			pname = p.find('div',{'class':'views-field views-field-title'})
			professorname = doc.createElement("professorname")
			professorname.appendChild(doc.createTextNode(pname.text))
			research.appendChild(professorname)
		institution.appendChild(research)
	doc.writexml(fout_xml, "\t", "\t", "\n")
	fout_xml.close()
	
		