# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os
import urllib
import xml.dom.minidom as minidom

class writePipeline(object):
    def __init__(self):
        self.fout_xml = file('test.xml','w')
        self.doc = minidom.Document()
        self.institution = self.doc.createElement("institution")
        self.doc.appendChild(self.institution)
        self.cnt = 0
        if(not os.path.exists('d:/PYPJ/pictures')):
            os.mkdir('d:/PYPJ/pictures')


    def process_item(self, item, spider):
            professor = self.doc.createElement("professor")
            self.institution.appendChild(professor)
            namenode = self.doc.createElement("name")
            namenode.appendChild(self.doc.createTextNode(item['name'].encode('utf-8')))
            professor.appendChild(namenode)

            websitenode = self.doc.createElement("website")
            websitenode.appendChild(self.doc.createTextNode(item['website'].encode('utf-8')))
            professor.appendChild(websitenode)

            phonenode = self.doc.createElement("phone")
            phonenode.appendChild(self.doc.createTextNode(item['phone'].encode('utf-8')))
            professor.appendChild(phonenode)

            officenode = self.doc.createElement("office")
            officenode.appendChild(self.doc.createTextNode(item['office'].encode('utf-8')))
            professor.appendChild(officenode)

            # piclocal = "d:/PYPJ/pictures/" + item['name'].encode('utf-8') + ".jpg"
            # urllib.urlretrieve(item['picture'], piclocal)
            picnode = self.doc.createElement("image")
            picnode.appendChild(self.doc.createTextNode("./images/" + item['name'].encode('utf-8') + ".jpg"))
            professor.appendChild(picnode)

            self.cnt += 1
    def close_spider(self, spider):
        print self.cnt
        self.doc.writexml(self.fout_xml, "\t", "\t", "\n")
        self.fout_xml.close()
