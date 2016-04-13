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

fout_xml = file('TAMU_research.xml', 'w')
doc = minidom.Document()
institution = doc.createElement("institution")
doc.appendChild(institution)

if __name__ == '__main__':
	url = 'http://engineering.tamu.edu/cse/research'
	html = urllib2.urlopen(url).read()
	soup = BeautifulSoup(html)
	cont = soup.find('div',{'class':'large-12 columns'})
	areaList = cont.findAll("li")
	for i in range(0,len(areaList)):
		research = doc.createElement("research")
		grouptext = areaList[i].text
		groupname = doc.createElement("groupname")
		groupname.appendChild(doc.createTextNode(grouptext))
		research.appendChild(groupname)
		groupurl = 'http://engineering.tamu.edu/'+areaList[i].find("a")['href']
		grouphtml = urllib2.urlopen(groupurl).read()
		groupsoup = BeautifulSoup(grouphtml)
		profList = groupsoup.findAll('p')
		for professor in profList:
			if professor.find("a") == None: continue
			professorname = doc.createElement("professorname")
			professorname.appendChild(doc.createTextNode(professor.find("a").text))
			research.appendChild(professorname)
			professor = professor.nextSibling
		institution.appendChild(research)
	doc.writexml(fout_xml, "\t", "\t", "\n")
	fout_xml.close()
	
		