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

fout_xml = file('Rutgers_research.xml', 'w')
doc = minidom.Document()
institution = doc.createElement("institution")
doc.appendChild(institution)

if __name__ == '__main__':
	url = 'http://www.cs.rutgers.edu/research/'
	html = urllib2.urlopen(url).read()
	soup = BeautifulSoup(html)
	cont = soup.find('ul',{'id':'da-thumbs'})
	areaList = cont.findAll("li")
	for i in range(0,len(areaList)):
		areaurl = url+areaList[i].find("a")['href']
		areahtml = urllib2.urlopen(areaurl).read()
		areasoup = BeautifulSoup(areahtml)
		subarea = areasoup.findAll('li',{'class':'research_subarea glow'})
		for sub in subarea:
			research = doc.createElement("research")
			sub.find('div',{'class':'block-inside'})
			grouptext = sub.text.strip()
			groupname = doc.createElement("groupname")
			groupname.appendChild(doc.createTextNode(grouptext))
			research.appendChild(groupname)
			suburl = url+sub.find("a")['href']
			subhtml = urllib2.urlopen(suburl).read()
			subsoup = BeautifulSoup(subhtml)
			prof = subsoup.find('div',{'class':'faculty_body'})
			professor = prof.findAll('div',{'class':"faculty_label"})
			for p in professor:
				professorname = doc.createElement("professorname")
				professorname.appendChild(doc.createTextNode(p.text.strip()))
				research.appendChild(professorname)
			institution.appendChild(research)
	doc.writexml(fout_xml, "\t", "\t", "\n")
	fout_xml.close()
	