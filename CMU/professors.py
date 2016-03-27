#!/usr/bin/python2

import urllib2
import HTMLParser
import sys
import xml.dom.minidom as minidom

fileLocation = './cmu_images'

class MyParser(HTMLParser.HTMLParser):
    def __init__(self):
        HTMLParser.HTMLParser.__init__(self)
        self.hasinfo = False
        self.namelist = []
        self.hastd = False
        self.hastr = False
        self.hasref = False
        self.imagelist = []
    def handle_starttag(self, tag, attrs):
        if tag == 'tr':
            self.hastr = True
        if tag == 'td':
            self.hastd = True
        if tag == 'a' and self.hastd == True:
            for key, value in attrs:
                if key == 'href':
                    self.tempinfo[0] = value
                    self.hasref = True
        if self.hastd == True and tag == 'img':
            for key, value in attrs:
                if key == 'src':
                    imgContent = urllib2.urlopen(value).read()
                    imgFileName = fileLocation + '/'+value.split('/')[-1]
                    imgFile = open(imgFileName, 'w')
                    imgFile.write(imgContent)
                    self.image_path = imgFileName

    def handle_data(self, text):
        if self.hasref:
            self.namelist.append(text)
    def handle_endtag(self, tag):
        if tag == 'tr':
            self.hastr = False
        if tag == 'td':
            self.hastd = False
        if self.hasref == True:
            self.hasref = False

rootUrl = 'http://www-cs.stanford.edu/directory/faculty'
response = urllib2.urlopen(rootUrl)
html = response.read()
my = MyParser()
my.feed(html)
    
fout_xml = file('CMU.xml','w')
doc = minidom.Document()
institution = doc.createElement("institution")
doc.appendChild(institution)
website_no = 0
for i in range(len(my.infolist)):
    if len(my.infolist[i][1]) == 0:
        continue
    professor = doc.createElement("professor")
    institution.appendChild(professor)
    
    name = my.infolist[i][1][0][0]
    namenode = doc.createElement("name")
    namenode.appendChild(doc.createTextNode(name))
    professor.appendChild(namenode)
    
    office = ''
    for x in my.infolist[i][1][2]:
        office = x+' '
    if office != '':
        officenode = doc.createElement("office")
        officenode.appendChild(doc.createTextNode(office[:-1]))
        professor.appendChild(officenode)
    
    phone = my.infolist[i][1][1]
    if len(phone) != 0:
        phonenode = doc.createElement("phone")
        phonenode.appendChild(doc.createTextNode(phone[0]))
        professor.appendChild(phonenode)
    
    website = my.infolist[i][0]
    if website != []:
        websitenode = doc.createElement("website")
        websitenode.appendChild(doc.createTextNode(website))
        professor.appendChild(websitenode)
        try:
            single_response = urllib2.urlopen(website)
            single_html = response.read()
            single = SingleParser()
            single.feed(single_html)
            if single.image_path != '':
                imagenode = doc.createElement("image")
                imagenode.appendChild(doc.createTextNode(image_path))
                professor.appendChild(imagenode)
        except:
            pass
    
    institution.appendChild(professor)
doc.writexml(fout_xml, "\t", "\t", "\n")

fout_xml.close()


