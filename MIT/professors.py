#!/usr/bin/python2

import urllib2
import HTMLParser
import sys
import xml.dom.minidom as minidom

fileLocation = './mit_images'
class MyParser(HTMLParser.HTMLParser):
    def __init__(self):
        HTMLParser.HTMLParser.__init__(self)
        self.photo = False
        self.hasname = False
        self.hastitle = False
        self.hasemail = False
        self.hasoffice = False
        self.hasphone = False
        self.namelist = []
        self.imagelist = []
        self.titlelist = []
        self.officelist = []
        self.phonelist = []
        self.emaillist = []
        self.websitelist = []
        self.tempname = []
        self.temptitle = []
        self.tempoffice = []
        self.tempphone= []
        self.tempemail = []
        
    def handle_starttag(self, tag, attrs):
        if tag == 'div':
            for name, value in attrs:
                if name == 'class':
                    if value == 'views-field views-field-field-person-photo':
                        self.photo = True
                    if value == 'views-field views-field-title':
                        self.hasname = True
                    if value == 'views-field views-field-field-person-title':
                        self.hastitle = True
                    if value == 'views-field views-field-field-person-email':
                        self.hasemail = True
                    if value == 'views-field views-field-field-person-phone':
                        self.hasphone = True
                    if value == 'views-field views-field-field-person-office':
                        self.hasoffice = True
        if tag == 'img' and self.photo == True:
            for name, value in attrs:
                if name == 'src':
                    #imgContent = urllib2.urlopen('https:'+value).read()
                    imgFileName = fileLocation+'/'+value.split('/')[-1]
                    #imgFile = open(imgFileName, 'w')
                    #imgFile.write(imgContent)
                    self.imagelist.append(imgFileName)
                    #imgFile.close()
        if self.hasname == True:
            if tag == 'a':
                for name, value in attrs:
                    if name == 'href':
                        self.websitelist.append(value)
            if tag == 'span':
                self.websitelist.append('span')
    
    def handle_data(self, text):
        if self.hasname:
            if text != '' and text.isspace() == False:
                self.tempname.append(text)
        if self.hastitle:
            if text != '' and text.isspace() == False:
                self.temptitle.append(text)
        if self.hasoffice:
            if text != '' and text.isspace() == False:
                self.tempoffice.append(text)
        if self.hasphone:
            if text != '' and text.isspace() == False:
                self.tempphone.append(text)
        if self.hasemail:
            if text != '' and text.isspace() == False:
                self.tempemail.append(text)
    
    def handle_endtag(self, tag):
        if tag == 'div':
            self.photo = False
            if self.hasname:
                self.namelist.append(self.tempname)
                self.hasname = False
                self.tempname = []
            if self.hastitle:
                self.titlelist.append(self.temptitle)
                self.hastitle = False
                self.temptitle = []
            if self.hasemail:
                self.emaillist.append(self.tempemail)
                self.hasemail = False
                self.tempemail = []
            if self.hasoffice:
                self.officelist.append(self.tempoffice)
                self.hasoffice = False
                self.tempoffice = []
            if self.hasphone:
                self.phonelist.append(self.tempphone)
                self.hasphone = False
                self.tempphone = []

rootUrl = 'https://www.eecs.mit.edu/people/faculty-advisors'
response = urllib2.urlopen(rootUrl)
html = response.read()
my = MyParser()
my.feed(html)

#fout = open('out.txt','w')
#for i in range(len(my.namelist)):
#    name = my.namelist[i]
#    titles = my.titlelist[i]
#    image_path = my.imagelist[i]
#    fout.write(name[0]+'\n')
#    for title in titles:
#        fout.write(title+'\n')
#    fout.write(image_path+'\n\n')
    
fout_xml = file('MIT.xml','w')
doc = minidom.Document()
institution = doc.createElement("institution")
doc.appendChild(institution)
website_no = 0
for i in range(len(my.namelist)):
    name = my.namelist[i][0]
    titles = my.titlelist[i]
    image_path = my.imagelist[i]
    phone = my.phonelist[i][0]
    email = my.emaillist[i][0]
    office = my.officelist[i][0]

    professor = doc.createElement("professor")
    institution.appendChild(professor)
    
    namenode = doc.createElement("name")
    namenode.appendChild(doc.createTextNode(name))
    professor.appendChild(namenode)
    
    for title in titles:
        titlenode = doc.createElement("title")
        titlenode.appendChild(doc.createTextNode(title))
        professor.appendChild(titlenode)
    
    imagenode = doc.createElement("image")
    imagenode.appendChild(doc.createTextNode(image_path))
    professor.appendChild(imagenode)
    
    officenode = doc.createElement("office")
    officenode.appendChild(doc.createTextNode(office))
    professor.appendChild(officenode)
    
    
    phonenode = doc.createElement("phone")
    phonenode.appendChild(doc.createTextNode(phone))
    professor.appendChild(phonenode)
    
    emailnode = doc.createElement("email")
    emailnode.appendChild(doc.createTextNode(email))
    professor.appendChild(emailnode)

    if website_no+1 < len(my.websitelist):
        if my.websitelist[website_no+1] != 'span':
            website = my.websitelist[website_no+1]
            websitenode = doc.createElement("website")
            websitenode.appendChild(doc.createTextNode(website))
            professor.appendChild(websitenode)
            website_no += 2
        else:
            website_no += 1
    institution.appendChild(professor)
doc.writexml(fout_xml, "\t", "\t", "\n")

#fout.close()
fout_xml.close()


