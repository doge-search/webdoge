#!/usr/bin/python2
#coding=utf-8

import urllib2
import HTMLParser
import sys
import xml.dom.minidom as minidom
from htmlentitydefs import entitydefs
import glob

reload(sys)
sys.setdefaultencoding('utf8')
class MyParser(HTMLParser.HTMLParser):
    def __init__(self):
        HTMLParser.HTMLParser.__init__(self)
        self.hasfirstname = False
        self.haslastname = False
        self.firstnamelist = []
        self.lastnamelist = []
    def handle_starttag(self, tag, attrs):
        if tag == 'div':
            for key, value in attrs:
                if key == 'class':
                    if value == "field field-name-field-first-name field-type-text field-label-hidden":
                        self.hasfirstname = True
                    if value == "field field-name-field-last-name field-type-text field-label-hidden":
                        self.haslastname = True
    def handle_data(self, text):
        if self.hasfirstname and text.isspace() == False:
            self.firstnamelist.append(text)
        if self.haslastname and text.isspace() == False:
            self.lastnamelist.append(text)
    def handle_endtag(self, tag):
        if tag == 'div' and self.hasfirstname == True:
            self.hasfirstname = False
        if tag == 'div' and self.haslastname == True:
            self.haslastname = False

fout_xml = file('Colorado.xml','w')
doc = minidom.Document()
institution = doc.createElement("institution")
doc.appendChild(institution)

if True:
    rootUrl = 'http://www.colorado.edu/cs/our-people?field_person_type_tid=1'
    response = urllib2.urlopen(rootUrl)
    html = response.read()
    my = MyParser()
    my.feed(html)
    for i in range(len(my.firstnamelist)):
        professor = doc.createElement("professor")
        institution.appendChild(professor)
    
        name = my.firstnamelist[i] + ' ' + my.lastnamelist[i]
        namenode = doc.createElement("name")
        namenode.appendChild(doc.createTextNode(name))
        professor.appendChild(namenode)
    
        institution.appendChild(professor)

doc.writexml(fout_xml, "\t", "\t", "\n")

fout_xml.close()



