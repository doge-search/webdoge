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

fout_xml = file('Wustl_research.xml', 'w')
doc = minidom.Document()
institution = doc.createElement("institution")
doc.appendChild(institution)

def after(text):
    i=0
    while text[i] == ' ' or text[i] == '\t' or text[i] == '\n':
        i+=1
    j=-1
    while text[j] == ' ' or text[j] == '\t' or text[j] == '\n':
        j-=1
    return text[i:j+1]

if __name__ == '__main__':
    url = 'http://cse.wustl.edu/Research/labs/Pages/labs.aspx'
    html = urllib2.urlopen(url).read()
    html = unicode(html,'gb2312','ignore').encode('utf-8','ignore')
    soup = BeautifulSoup(html)
    areaList = soup.findAll('li')
    for area in areaList:
        area = area.find('a')
        if 'target' in area.attrs and 'href' in area.attrs:
            research = doc.createElement("research")
            groupname = doc.createElement("groupname") 
            groupname.appendChild(doc.createTextNode(after(area.text)))
            research.appendChild(groupname)
            import IPython
            IPython.embed()
            newurl = area.attrs['href']
            newhtml = urllib2.urlopen(newurl).read()
            newhtml = unicode(newhtml,'gb2312','ignore').encode('utf-8','ignore')
            newsoup = BeautifulSoup(newhtml)
            professors = newsoup.findAll('div',{'class':'person-profile'})
            for j in professors:
                x = j.findAll('a')[1]
                professorname = doc.createElement("professorname")
                professorname.appendChild(doc.createTextNode(x.text))
	        research.appendChild(professorname)
	    institution.appendChild(research)
    doc.writexml(fout_xml, "\t", "\t", "\n")
    fout_xml.close()
	
		
