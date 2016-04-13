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

fout_xml = file('RPI_research.xml', 'w')
doc = minidom.Document()
institution = doc.createElement("institution")
doc.appendChild(institution)

if __name__ == '__main__':
	url = 'http://www.cs.rpi.edu/research/groups.html'
	html = urllib2.urlopen(url).read()
	soup = BeautifulSoup(html)
	areaList = soup.findAll('p',{'class':'itemHead'})
	profList = soup.findAll('p',{'class':'faculty'})
	for i in range(0,len(areaList)):
		research = doc.createElement("research")
		grouptext = areaList[i].text
		groupname = doc.createElement("groupname")
		groupname.appendChild(doc.createTextNode(grouptext))
		research.appendChild(groupname)
		#groupurl = 'http://www.cs.rochester.edu/research/'+areaList[i].find("a")['href']
		#grouphtml = urllib2.urlopen(groupurl).read()
		#groupsoup = BeautifulSoup(grouphtml)
		#professor = groupsoup.findAll("dt")
		professor = profList[i].findAll("a")
		for p in professor:
			professorname = doc.createElement("professorname")
			professorname.appendChild(doc.createTextNode(p.text))
			research.appendChild(professorname)
		institution.appendChild(research)
	doc.writexml(fout_xml, "\t", "\t", "\n")
	fout_xml.close()
	
		