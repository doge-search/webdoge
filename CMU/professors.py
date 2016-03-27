#!/usr/bin/python2
#coding=utf-8

import urllib2
import HTMLParser
import sys
import xml.dom.minidom as minidom
from htmlentitydefs import entitydefs
import glob

fileLocation = './cmu_images'

class MyParser(HTMLParser.HTMLParser):
    def __init__(self):
        HTMLParser.HTMLParser.__init__(self)
        self.hasinfo = False
        self.infolist = []
        self.hastd = False
        self.hastr = False
        self.hasref = False
        self.haslastname = False
        self.hasfirstname = False
        self.hastitle = False
        self.hasoffice = False
        self.hasemail = False
        self.hasphone = False
        self.tempinfo = [[],[],[], [], [], [], []]
    def handle_starttag(self, tag, attrs):
        if tag == 'tr':
            self.hastr = True
        if tag == 'td':
            self.hastd = True
            for key, value in attrs:
                if key == 'class':
                    if value == 'views-field views-field-field-last-name active':
                        self.haslastname = True
                    if value == 'views-field views-field-field-computed-first':
                        self.hasfirstname = True
                    if value == 'views-field views-field-field-computed-title':
                        self.hastitle = True    
                    if value == 'views-field views-field-field-computed-building':
                        self.hasoffice = True
                    if value == 'views-field views-field-field-computed-email':
                        self.hasemail = True
                    if value == 'views-field views-field-field-computed-phone':
                        self.hasphone = True
        if tag == 'a' and self.haslastname == True:
            for key, value in attrs:
                if key == 'href':
                    self.tempinfo[6] ='https://www.scs.cmu.edu' + value 
    def handle_entityref(self, name):
        if entitydefs.has_key(name):
            self.handle_data(entitydefs[name])
        else:
            self.handle_data('&'+name+';')
    def handle_data(self, text):
        if self.haslastname and text.isspace() == False:
            self.tempinfo[0] = text
        if self.hasfirstname and text.isspace() == False:
            self.tempinfo[1] = text
        if self.hastitle and text.isspace() == False:
            self.tempinfo[2] = text
        if self.hasoffice and text.isspace() == False:
            self.tempinfo[3] = text
        if self.hasemail and text.isspace() == False:
            self.tempinfo[4].append(text)
        if self.hasphone and text.isspace() == False:
            self.tempinfo[5] = text
    def handle_endtag(self, tag):
        if tag == 'tr':
            self.hastr = False
            if self.tempinfo[0] != []:
                self.infolist.append(self.tempinfo)
                self.tempinfo = [[],[],[], [], [], [], []]
        if tag == 'td':
            self.hastd = False
            self.haslastname = False
            self.hasfirstname = False
            self.hastitle = False
            self.hasoffice = False
            self.hasemail = False
            self.hasphone = False

def delspace(string):
    begin = 0
    end = -1
    while True:
        if string[begin] == '\n' or string[begin] == ' ':
            begin += 1
        else:
            break
    while True:
        if string[end] == '\n' or string[end] == ' ':
            end -= 1
        else:
            break
    if end != -1:
        return string[begin:end+1]
    else:
        return string[begin:]

fout_xml = file('CMU.xml','w')
doc = minidom.Document()
institution = doc.createElement("institution")
doc.appendChild(institution)
#rootUrl = 'https://www.scs.cmu.edu/directory/all'
#response = urllib2.urlopen(rootUrl)
html_files = glob.glob('./factory/*.html')
for html_file in html_files:
    f = open(html_file, 'r')
    html = f.read()
    my = MyParser()
    my.feed(html)
    f.close()
    for i in range(len(my.infolist)):
        professor = doc.createElement("professor")
        institution.appendChild(professor)
    
        name = delspace(my.infolist[i][1]) + ' ' + my.infolist[i][0]
        namenode = doc.createElement("name")
        namenode.appendChild(doc.createTextNode(name))
        professor.appendChild(namenode)
    
        title = delspace(my.infolist[i][2])
        titlenode = doc.createElement("title")
        titlenode.appendChild(doc.createTextNode(title))
        professor.appendChild(titlenode)
    
        if len(my.infolist[i][3]) > 0:
            office = delspace(my.infolist[i][3])
            officenode = doc.createElement("office")
            officenode.appendChild(doc.createTextNode(office))
            professor.appendChild(officenode)
    
        if len(my.infolist[i][4]) == 3:
            email = my.infolist[i][4][0] + '@'+my.infolist[i][4][2]
            emailnode = doc.createElement("email")
            emailnode.appendChild(doc.createTextNode(email))
            professor.appendChild(emailnode)
        if len(my.infolist[i][5]) > 0:
            phone = delspace(my.infolist[i][5])
            phonenode = doc.createElement("phone")
            phonenode.appendChild(doc.createTextNode(phone))
            professor.appendChild(phonenode)
    
        website = my.infolist[i][6]
        websitenode = doc.createElement("website")
        websitenode.appendChild(doc.createTextNode(website))
        professor.appendChild(websitenode)
    
        #image = my.infolist[i][0]
        #imagenode = doc.createElement("image")
        #imagenode.appendChild(doc.createTextNode(image))
        #professor.appendChild(imagenode)
    
        institution.appendChild(professor)

doc.writexml(fout_xml, "\t", "\t", "\n")

fout_xml.close()


