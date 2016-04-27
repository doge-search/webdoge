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

fout_xml = file('StonyBrook_research.xml', 'w')
doc = minidom.Document()
institution = doc.createElement("institution")
doc.appendChild(institution)

if __name__ == '__main__':
    url = 'https://www.cs.stonybrook.edu/research'
    html = urllib2.urlopen(url).read()
    html = unicode(html,'gb2312','ignore').encode('utf-8','ignore')
    soup = BeautifulSoup(html)
    areaList = soup.findAll('div',{'class':'item-list'})[0]
    allgroups = areaList.findAll('li')
    for i, group in enumerate(allgroups):
        research = doc.createElement("research")
        groupname = doc.createElement("groupname") 
        groupname.appendChild(doc.createTextNode(group.text))
        research.appendChild(groupname)
        newurl = 'https://www.cs.stonybrook.edu/research?qt-lab_tabs='+str(i)+'#qt-lab_tabs'
        newhtml = urllib2.urlopen(newurl).read()
        newhtml = unicode(newhtml,'gb2312','ignore').encode('utf-8','ignore')
        newsoup = BeautifulSoup(newhtml)
        professorList = newsoup.findAll('div',{'id':'quicktabs-tabpage-lab_tabs-'+str(i)})[0]
        professors = professorList.findAll('div',{'class':'views-field views-field-title'})
        for j in professors:
            professorname = doc.createElement("professorname")
            professorname.appendChild(doc.createTextNode(j.text))
	    research.appendChild(professorname)
	institution.appendChild(research)
    doc.writexml(fout_xml, "\t", "\t", "\n")
    fout_xml.close()
	
		
