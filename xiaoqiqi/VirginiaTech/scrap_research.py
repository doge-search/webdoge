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

fout_xml = file('VirginiaTech_research.xml', 'w')
doc = minidom.Document()
institution = doc.createElement("institution")
doc.appendChild(institution)

if __name__ == '__main__':
	url = 'http://www.cs.vt.edu/research'
	html = urllib2.urlopen(url).read()
	soup = BeautifulSoup(html)
	content = soup.find('div',{'id':'research'})
	areaList = content.findAll('div',{'class':'area'})
	for i in range(len(areaList)):
		research = doc.createElement("research")
		grouptext = areaList[i].find("h4").find("a").string
		groupname = doc.createElement("groupname")
		groupname.appendChild(doc.createTextNode(grouptext))
		research.appendChild(groupname)
		#groupurl = areaList[i]['href']
		#grouphtml = urllib2.urlopen(groupurl).read()
		#groupsoup = BeautifulSoup(grouphtml)
		professor = areaList[i].findAll('a',{'class':'faculty'})
		for p in professor:
			professorname = doc.createElement("professorname")
			professorname.appendChild(doc.createTextNode(p.string))
			research.appendChild(professorname)
		institution.appendChild(research)
	doc.writexml(fout_xml, "\t", "\t", "\n")
	fout_xml.close()
	
		