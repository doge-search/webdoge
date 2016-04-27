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

fout_xml = file('UCB_research.xml', 'w')
doc = minidom.Document()
institution = doc.createElement("institution")
doc.appendChild(institution)

if __name__ == '__main__':
    url = 'http://www.eecs.berkeley.edu/Research/Areas/'
    html = urllib2.urlopen(url).read()
    html = unicode(html,'gb2312','ignore').encode('utf-8','ignore')
    soup = BeautifulSoup(html)
    areaList = soup.findAll('ul',{'class':'index'})[0]
    allgroups = areaList.findAll('li')
    for i, group in enumerate(allgroups):
        research = doc.createElement("research")
        groupname = doc.createElement("groupname") 
        groupname.appendChild(doc.createTextNode(group.text))
        research.appendChild(groupname)
        newurl = 'http://www.eecs.berkeley.edu'+group.find('a').attrs['href']
        newhtml = urllib2.urlopen(newurl).read()
        newhtml = unicode(newhtml,'gb2312','ignore').encode('utf-8','ignore')
        newsoup = BeautifulSoup(newhtml)
        allul = newsoup.findAll('ul')
        for ul in allul:
            x=ul.findAll('a')
            for professor in x:
                if professor.attrs['href'][:8] != '/Faculty':
                    break
                professorname = doc.createElement("professorname")
                professorname.appendChild(doc.createTextNode(professor.text))
	        research.appendChild(professorname)
	institution.appendChild(research)
    doc.writexml(fout_xml, "\t", "\t", "\n")
    fout_xml.close()
	
		
