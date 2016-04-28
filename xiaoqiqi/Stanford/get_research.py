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

fout_xml = file('Stanford_research.xml', 'w')
doc = minidom.Document()
institution = doc.createElement("institution")
doc.appendChild(institution)

if __name__ == '__main__':
    f = open('Stanford_research.txt','r')
    lines = f.readlines()
    line_no = 0
    flag = 1
    while line_no < len(lines):
        line =lines[line_no]
        if flag == 1:
	    research = doc.createElement("research")
	    groupname = doc.createElement("groupname")
            groupname.appendChild(doc.createTextNode(line[:-1]))
	    research.appendChild(groupname)
            flag = 0
        else:
            if line == '\n':
                if flag == 0:
                    institution.appendChild(research)
                    flag = 1
            else:
                professorname = doc.createElement("professorname")
                professorname.appendChild(doc.createTextNode(line[:-1]))
	        research.appendChild(professorname)
	line_no += 1
        institution.appendChild(research)
    doc.writexml(fout_xml, "\t", "\t", "\n")
    fout_xml.close()
	
		
