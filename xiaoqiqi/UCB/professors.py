#!/usr/bin/python2
#coding=utf-8

import urllib2
import HTMLParser
import sys
import xml.dom.minidom as minidom
from htmlentitydefs import entitydefs

fileLocation = './ucb_images'

class MyParser(HTMLParser.HTMLParser):
    def __init__(self):
        HTMLParser.HTMLParser.__init__(self)
        self.hasinfo = False
        self.infolist = []
        self.hastd = False
        self.hastr = False
        self.hasref = False
        self.hascolspan = False
        self.tempinfo = [[],[],[]]
        #image, website, name, title 
    def handle_starttag(self, tag, attrs):
        if tag == 'tr':
            self.hastr = True
        if tag == 'td':
            self.hastd = True
            for key, value in attrs:
                if key == 'colspan' and value == '2':
                    self.hascolspan = True
        if tag == 'a' and self.hascolspan == True:
            for key, value in attrs:
                if key == 'href':
                    self.tempinfo[1] = 'http://www.eecs.berkeley.edu' + value
                    self.hasref = True
        if self.hastd == True and tag == 'img':
            for key, value in attrs:
                if key == 'src':
                    imgContent = urllib2.urlopen(value).read()
                    imgFileName = fileLocation + '/'+value.split('/')[-1]
                    imgFile = open(imgFileName, 'w')
                    imgFile.write(imgContent)
                    self.tempinfo[0] = imgFileName
    def handle_entityref(self, name):
        if entitydefs.has_key(name):
            self.handle_data(entitydefs[name])
        else:
            self.handle_data('&'+name+';')
    def handle_data(self, text):
        if self.hasref:
            self.tempinfo[2].append(text)
    def handle_endtag(self, tag):
        if tag == 'tr':
            self.hastr = False
            if self.tempinfo[0] != []:
                self.infolist.append(self.tempinfo)
                self.tempinfo = [[],[],[]]
        if tag == 'td':
            self.hastd = False
        if self.hasref == True: 
            self.hasref = False
            self.hascolspan = False
rootUrl = 'http://www.eecs.berkeley.edu/Faculty/Lists/CS/list.shtml'
response = urllib2.urlopen(rootUrl)
html = response.read()
my = MyParser()
my.feed(html)

fout_xml = file('UCB.xml','w')
doc = minidom.Document()
institution = doc.createElement("institution")
doc.appendChild(institution)
website_no = 0
for i in range(len(my.infolist)):
    professor = doc.createElement("professor")
    institution.appendChild(professor)
    
    name = ''
    for namepart in my.infolist[i][2]:
        name += namepart
    namenode = doc.createElement("name")
    namenode.appendChild(doc.createTextNode(name))
    professor.appendChild(namenode)
    
    website = my.infolist[i][1]
    websitenode = doc.createElement("website")
    websitenode.appendChild(doc.createTextNode(website))
    professor.appendChild(websitenode)
    
    image = my.infolist[i][0]
    imagenode = doc.createElement("image")
    imagenode.appendChild(doc.createTextNode(image))
    professor.appendChild(imagenode)
    
    institution.appendChild(professor)
doc.writexml(fout_xml, "\t", "\t", "\n")

fout_xml.close()


