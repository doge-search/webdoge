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
        self.hasref = False
        self.hasimg = False
        self.needpass = False
        self.namelist = []
    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            for key, value in attrs:
                if key == 'href':
                    if self.hasimg == True:
                        self.hasname = True
                    self.hasref = True
        if tag == 'img' and self.hasref == True:
            self.hasimg = True
        if tag == 'div':
            for key, value in attrs:
                if key == 'class' and value == 'notes':
                    self.needpass = True
    #def handle_entityref(self, name):
    #    if entitydefs.has_key(name):
    #        self.handle_data(entitydefs[name])
    #    else:
    #        self.handle_data('&'+name+';')
    def handle_data(self, text):
        if self.hasimg and self.needpass==False and text.isspace() == False:
            self.namelist.append(text)
    def handle_endtag(self, tag):
        if tag == 'a' and self.hasref == True:
            self.hasref = False
        if tag == 'a' and self.hasname == True:
            self.hasname = False
            self.hasimg = False
        if tag == 'div' and self.needpass == True:
            self.needpass = False
fout_xml = file('Arizona.xml','w')
doc = minidom.Document()
institution = doc.createElement("institution")
doc.appendChild(institution)

if True:
    rootUrl = 'http://www.cs.arizona.edu/personnel/faculty.html'
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



