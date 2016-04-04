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
        self.hasname = False
        self.namelist = []
    def handle_starttag(self, tag, attrs):
        if tag == 'tr':
            for key, value in attrs:
                if key == 'class':
                    if value == "odd" or value == 'even' or value == 'odd views-row-first':
                        self.hasname = True
    #def handle_entityref(self, name):
    #    if entitydefs.has_key(name):
    #        self.handle_data(entitydefs[name])
    #    else:
    #        self.handle_data('&'+name+';')
    def handle_data(self, text):
        if self.hasname and text.isspace() == False:
            self.namelist.append(text)
    def handle_endtag(self, tag):
        if tag == 'td' and self.hasname == True:
            self.hasname = False

fout_xml = file('UChicage.xml','w')
doc = minidom.Document()
institution = doc.createElement("institution")
doc.appendChild(institution)

if True:
    rootUrl = 'https://cs.uchicago.edu/directories/table/faculty'
    response = urllib2.urlopen(rootUrl)
    html = response.read()
    my = MyParser()
    my.feed(html)
    for i in range(len(my.namelist)):
        professor = doc.createElement("professor")
        institution.appendChild(professor)
    
        name = my.namelist[i]
        namenode = doc.createElement("name")
        namenode.appendChild(doc.createTextNode(name))
        professor.appendChild(namenode)
    
        institution.appendChild(professor)

doc.writexml(fout_xml, "\t", "\t", "\n")

fout_xml.close()



