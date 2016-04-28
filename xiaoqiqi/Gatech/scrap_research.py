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

fout_xml = file('Gatech_research.xml', 'w')
doc = minidom.Document()
institution = doc.createElement("institution")
doc.appendChild(institution)

if __name__ == '__main__':
	url = 'http://www.scs.gatech.edu/research/research-areas'
	html = urllib2.urlopen(url).read()
	soup = BeautifulSoup(html)
	content = soup.find('div',{'class':'body'})
	cont = content.find('ul')
	areaList = cont.findAll("a")
	for i in range(len(areaList)):
		if i == 1:continue
		research = doc.createElement("research")
		grouptext = areaList[i].text
		groupname = doc.createElement("groupname")
		groupname.appendChild(doc.createTextNode(grouptext))
		research.appendChild(groupname)
		groupurl = areaList[i]['href']
		grouphtml = urllib2.urlopen(groupurl).read()
		groupsoup = BeautifulSoup(grouphtml)
		prof = groupsoup.find('div',{'class':'body'})
		professor = prof.findAll("li")
		for p in professor:
			professorname = doc.createElement("professorname")
			professorname.appendChild(doc.createTextNode(p.text))
			research.appendChild(professorname)
		institution.appendChild(research)
	doc.writexml(fout_xml, "\t", "\t", "\n")
	fout_xml.close()
	
		