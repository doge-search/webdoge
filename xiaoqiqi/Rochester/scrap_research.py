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

fout_xml = file('Rochester_research.xml', 'w')
doc = minidom.Document()
institution = doc.createElement("institution")
doc.appendChild(institution)

if __name__ == '__main__':
	url = 'http://www.cs.rochester.edu/research/index.html'
	html = urllib2.urlopen(url).read()
	soup = BeautifulSoup(html)
	cont = soup.find('ul',{'class':'side-nav'})
	areaList = cont.findAll("li")
	for i in range(1,5):
		research = doc.createElement("research")
		grouptext = areaList[i].text
		groupname = doc.createElement("groupname")
		groupname.appendChild(doc.createTextNode(grouptext))
		research.appendChild(groupname)
		groupurl = 'http://www.cs.rochester.edu/research/'+areaList[i].find("a")['href']
		grouphtml = urllib2.urlopen(groupurl).read()
		groupsoup = BeautifulSoup(grouphtml)
		professor = groupsoup.findAll("dt")
		for p in professor:
			professorname = doc.createElement("professorname")
			professorname.appendChild(doc.createTextNode(p.text))
			research.appendChild(professorname)
		institution.appendChild(research)
	doc.writexml(fout_xml, "\t", "\t", "\n")
	fout_xml.close()
	
		