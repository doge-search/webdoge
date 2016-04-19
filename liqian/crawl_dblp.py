#!/usr/bin/python
#coding=utf-8
import dblp
import urllib2
import HTMLParser
import sys
import xml.dom.minidom as minidom
from htmlentitydefs import entitydefs
from lxml import etree
try:
	import xml.etree.cElementTree as ET
except ImportError:
	import xml.etree.ElementTree as ET
import glob
import os

reload(sys)
profname = 'aaa'
sys.setdefaultencoding('utf-8')
schools = ['brown', 'Caltech', 'columbia', 'duke', 'harvard', 'JHU', 'northwestern', 'NYU', 'OSU',
			'PSU', 'purdue', 'rice', 'UCI', 'UCLA', 'UCSD', 'UMASS', 'UMD', 'umich', 'UMN', 'UNC',
			'upenn', 'USC', 'virginia', 'WISC', 'yale']
def search(ini_name):
	name = ini_name.strip()
	nname = name.split(',')
	if len(nname) > 1:
		name = nname[1] + ' ' + nname[0]
	authors = dblp.search(' ' + name + ' ')
	if not authors:
		print "not found: " + name
		return (ini_name, -1)
	else:
		if len(authors) > 10:
			print "multiple: " + str(len(authors)) + ' ' + name

	cnt = 0
	index = 0
	if len(authors) > 1:
		for indx in range(len(authors)):
			if authors[indx].name == name:
				#print "match!" + name
				break
			index += 1
		if index == len(authors):
			print "not found in the list!" + name + ' compare with ' + authors[0].name + ' use default 0...'
			index = 0

	publications = authors[index].publications
	profname = authors[index].name
	for pub in publications:
		try: idx = pub.authors.index(profname)
		except ValueError:
			split_name = profname.split(' ')
			#profname = split_name[0] + ' ' + split_name[1][0] + '. ' + split_name[-1] #change middle name
			idx = 0
			for i in range(len(pub.authors)):
				pub_split = pub.authors[i].split(' ')
				if pub_split[0] == split_name[0] and pub_split[-1] == split_name[-1]:
					break
				idx += 1
			if idx == len(pub.authors):
				print pub.title
				print pub.authors
				idx = -1

		if idx >= 0:
			cnt += 1.0 / (idx + 1)
	return (ini_name, cnt)


if __name__ == "__main__":
	for school in schools:
		print "=== start crawling school:" + school
		filename = school + '/' + school + '.xml'
		if not os.path.isfile(filename):
			print "cannot find: " + filename
			continue
		tree = ET.ElementTree(file = filename)
		fout_xml = file(school+'/'+school+'_sort.xml', 'w')
		doc = minidom.Document()
		institution = doc.createElement("institution")
		doc.appendChild(institution)

		for prof in tree.getroot():
			for info in prof:
				if info.tag == 'name':
					name, cnt = search(info.text)
					print school + ': ' + name + ' with score: ' + "%.4f" % cnt
					professor = doc.createElement("professor")
					namenode = doc.createElement("name")
					namenode.appendChild(doc.createTextNode(name))
					professor.appendChild(namenode)
					papernode = doc.createElement("papers")
					papernode.appendChild(doc.createTextNode(str(cnt)))
					professor.appendChild(papernode)
					institution.appendChild(professor)
		doc.writexml(fout_xml, "\t", "\t", "\n")
		fout_xml.close()
		print "=== finished crawling: " + school 

