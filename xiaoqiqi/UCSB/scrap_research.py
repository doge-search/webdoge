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

fout_xml = file('UCSB_research.xml', 'w')
doc = minidom.Document()
institution = doc.createElement("institution")
doc.appendChild(institution)

if __name__ == '__main__':
    url = 'http://www.cs.ucsb.edu/research'
    html = urllib2.urlopen(url).read()
    html = unicode(html,'gb2312','ignore').encode('utf-8','ignore')
    soup = BeautifulSoup(html)
    areaList = soup.findAll('div',{'class':'field field-name-title'})
    for i, group in enumerate(areaList):
        research = doc.createElement("research")
        groupname = doc.createElement("groupname") 
        groupname.appendChild(doc.createTextNode(group.text))
        research.appendChild(groupname)
        newurl = 'http://www.cs.ucsb.edu'+group.find('a').attrs['href']
        newhtml = urllib2.urlopen(newurl).read()
        newhtml = unicode(newhtml,'gb2312','ignore').encode('utf-8','ignore')
        newsoup = BeautifulSoup(newhtml)
        professorList = newsoup.findAll('div',{'class':'field field-name-title'})
        for j in professorList:
            professorname = doc.createElement("professorname")
            professorname.appendChild(doc.createTextNode(j.text))
	    research.appendChild(professorname)
	institution.appendChild(research)
    doc.writexml(fout_xml, "\t", "\t", "\n")
    fout_xml.close()
	
		
