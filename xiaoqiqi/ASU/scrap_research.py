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

fout_xml = file('ASU_research.xml', 'w')
doc = minidom.Document()
institution = doc.createElement("institution")
doc.appendChild(institution)

if __name__ == '__main__':
	url = 'http://ecee.engineering.asu.edu/faculty-by-research-area/'
	html = urllib2.urlopen(url).read()
	html = unicode(html,'gb2312','ignore').encode('utf-8','ignore')
	soup = BeautifulSoup(html)
	areaList = soup.findAll('div',{'class':'et_pb_text et_pb_bg_layout_light et_pb_text_align_left'})
	for i in range(1,len(areaList)):
		research = doc.createElement("research")
		group = areaList[i].findAll("strong")
		groupname = doc.createElement("groupname")
		groupname.appendChild(doc.createTextNode(group[0].text))
		research.appendChild(groupname)
		professor = areaList[i].findAll("p")
		for i in professor:
			professorname = doc.createElement("professorname")
			professorname.appendChild(doc.createTextNode(i.text))
			research.appendChild(professorname)
		institution.appendChild(research)
	doc.writexml(fout_xml, "\t", "\t", "\n")
	fout_xml.close()
	
		