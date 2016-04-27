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

fout_xml = file('CMU_research.xml', 'w')
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

    research = doc.createElement("research")
    groupname = doc.createElement("groupname")
    groupname.appendChild(doc.createTextNode("Computational Biology Department"))
    research.appendChild(groupname)
    for i in range(0,1):
        url = ' https://www.cs.cmu.edu/directory/cbd?term_node_tid_depth=10571&page='+str(i)
        html = urllib2.urlopen(url).read()
	html = unicode(html,'gb2312','ignore').encode('utf-8','ignore')
	soup = BeautifulSoup(html)
        professor_last = soup.findAll('td',{'class':'views-field views-field-field-last-name active'})
        professor_first = soup.findAll('td',{'class':'views-field views-field-field-computed-first'})
        for i in range(len(professor_last)):
	    last = professor_last[i]
            first = professor_first[i]
            professorname = doc.createElement("professorname")
	    professorname.appendChild(doc.createTextNode(after(first.text)+' '+after(last.text)))
	    research.appendChild(professorname)
    institution.appendChild(research)
    
    research = doc.createElement("research")
    groupname = doc.createElement("groupname")
    groupname.appendChild(doc.createTextNode("Computer Science Department"))
    research.appendChild(groupname)
    for i in range(0,3):
        url = ' https://www.cs.cmu.edu/directory/csd?term_node_tid_depth=10571&page='+str(i)
        html = urllib2.urlopen(url).read()
	html = unicode(html,'gb2312','ignore').encode('utf-8','ignore')
	soup = BeautifulSoup(html)
        professor_last = soup.findAll('td',{'class':'views-field views-field-field-last-name active'})
        professor_first = soup.findAll('td',{'class':'views-field views-field-field-computed-first'})
        for i in range(len(professor_last)):
	    last = professor_last[i]
            first = professor_first[i]
            professorname = doc.createElement("professorname")
	    professorname.appendChild(doc.createTextNode(after(first.text)+' '+after(last.text)))
	    research.appendChild(professorname)
    institution.appendChild(research)
    
    
    research = doc.createElement("research")
    groupname = doc.createElement("groupname")
    groupname.appendChild(doc.createTextNode("Human-Computer Interaction Institute"))
    research.appendChild(groupname)
    for i in range(0,2):
        url = 'https://www.cs.cmu.edu/directory/hcii?term_node_tid_depth=10571&page='+str(i)
        html = urllib2.urlopen(url).read()
	html = unicode(html,'gb2312','ignore').encode('utf-8','ignore')
	soup = BeautifulSoup(html)
        professor_last = soup.findAll('td',{'class':'views-field views-field-field-last-name active'})
        professor_first = soup.findAll('td',{'class':'views-field views-field-field-computed-first'})
        for i in range(len(professor_last)):
	    last = professor_last[i]
            first = professor_first[i]
            professorname = doc.createElement("professorname")
	    professorname.appendChild(doc.createTextNode(after(first.text)+' '+after(last.text)))
	    research.appendChild(professorname)
    institution.appendChild(research)
        
    research = doc.createElement("research")
    groupname = doc.createElement("groupname")
    groupname.appendChild(doc.createTextNode("Institute for Software Research"))
    research.appendChild(groupname)
    for i in range(0,2):
        url = 'https://www.cs.cmu.edu/directory/isr?term_node_tid_depth=10571&page='+str(i)
        html = urllib2.urlopen(url).read()
	html = unicode(html,'gb2312','ignore').encode('utf-8','ignore')
	soup = BeautifulSoup(html)
        professor_last = soup.findAll('td',{'class':'views-field views-field-field-last-name active'})
        professor_first = soup.findAll('td',{'class':'views-field views-field-field-computed-first'})
        for i in range(len(professor_last)):
	    last = professor_last[i]
            first = professor_first[i]
            professorname = doc.createElement("professorname")
	    professorname.appendChild(doc.createTextNode(after(first.text)+' '+after(last.text)))
	    research.appendChild(professorname)
    institution.appendChild(research)
    
    research = doc.createElement("research")
    groupname = doc.createElement("groupname")
    groupname.appendChild(doc.createTextNode("Language Technologies Institute"))
    research.appendChild(groupname)
    for i in range(0,2):
        url = 'https://www.cs.cmu.edu/directory/lti?term_node_tid_depth=10571&page='+str(i)
        html = urllib2.urlopen(url).read()
	html = unicode(html,'gb2312','ignore').encode('utf-8','ignore')
	soup = BeautifulSoup(html)
        professor_last = soup.findAll('td',{'class':'views-field views-field-field-last-name active'})
        professor_first = soup.findAll('td',{'class':'views-field views-field-field-computed-first'})
        for i in range(len(professor_last)):
	    last = professor_last[i]
            first = professor_first[i]
            professorname = doc.createElement("professorname")
	    professorname.appendChild(doc.createTextNode(after(first.text)+' '+after(last.text)))
	    research.appendChild(professorname)
    institution.appendChild(research)
    

    research = doc.createElement("research")
    groupname = doc.createElement("groupname")
    groupname.appendChild(doc.createTextNode("Machine Learning Department"))
    research.appendChild(groupname)
    for i in range(0,1):
        url = 'https://www.cs.cmu.edu/directory/mld?term_node_tid_depth=10571&page='+str(i)
        html = urllib2.urlopen(url).read()
	html = unicode(html,'gb2312','ignore').encode('utf-8','ignore')
	soup = BeautifulSoup(html)
        professor_last = soup.findAll('td',{'class':'views-field views-field-field-last-name active'})
        professor_first = soup.findAll('td',{'class':'views-field views-field-field-computed-first'})
        for i in range(len(professor_last)):
	    last = professor_last[i]
            first = professor_first[i]
            professorname = doc.createElement("professorname")
	    professorname.appendChild(doc.createTextNode(after(first.text)+' '+after(last.text)))
	    research.appendChild(professorname)
    institution.appendChild(research)
    
    
    research = doc.createElement("research")
    groupname = doc.createElement("groupname")
    groupname.appendChild(doc.createTextNode("Robotics Institute"))
    research.appendChild(groupname)
    for i in range(0,2):
        url = 'https://www.cs.cmu.edu/directory/ri?term_node_tid_depth=10571&page='+str(i)
        html = urllib2.urlopen(url).read()
	html = unicode(html,'gb2312','ignore').encode('utf-8','ignore')
	soup = BeautifulSoup(html)
        professor_last = soup.findAll('td',{'class':'views-field views-field-field-last-name active'})
        professor_first = soup.findAll('td',{'class':'views-field views-field-field-computed-first'})
        for i in range(len(professor_last)):
	    last = professor_last[i]
            first = professor_first[i]
            professorname = doc.createElement("professorname")
	    professorname.appendChild(doc.createTextNode(after(first.text)+' '+after(last.text)))
	    research.appendChild(professorname)
    institution.appendChild(research)
    
    doc.writexml(fout_xml, "\t", "\t", "\n")
    fout_xml.close()
    
