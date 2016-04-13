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

fout_xml = file('Boston_research.xml', 'w')
doc = minidom.Document()
institution = doc.createElement("institution")
doc.appendChild(institution)

if __name__ == '__main__':
	url = 'http://www.bu.edu/cs/research/research-groups/'
	html = urllib2.urlopen(url).read()
	html = unicode(html,'gb2312','ignore').encode('utf-8','ignore')
	soup = BeautifulSoup(html)
	area = soup.find('ul',{'class':'linklist'})
	areaList = area.findAll("li")
	for i in range(0,len(areaList)):
		if i == 1: continue
		research = doc.createElement("research")
		groupname = doc.createElement("groupname")
		nametext = areaList[i].find("strong").text
		groupname.appendChild(doc.createTextNode(nametext))
		research.appendChild(groupname)
		if nametext == "TCS": nametext = "theory"
		groupurl = "HTTP://www.bu.edu/cs/" + nametext + "/people/"
		print groupurl
		grouphtml = urllib2.urlopen(groupurl).read()
		grouphtml = unicode(grouphtml,'gb2312','ignore').encode('utf-8','ignore')
		groupsoup = BeautifulSoup(grouphtml)
		if nametext == "IVC":
			professor = groupsoup.findAll('h5')
		else:
			professor = groupsoup.findAll('p',{'style':'text-align: center;'})
		for p in professor:
			findname = p.findAll("a")
			length = len(findname)
			professorname = doc.createElement("professorname")
			professorname.appendChild(doc.createTextNode(findname[length-1].text))
			research.appendChild(professorname)
		institution.appendChild(research)
	doc.writexml(fout_xml, "\t", "\t", "\n")
	fout_xml.close()
	