#!/usr/bin/python
#coding=utf-8
import requests
from lxml import etree
from collections import namedtuple

DBLP_BASE_URL = 'http://dblp.uni-trier.de/'
DBLP_AUTHOR_SEARCH_URL = DBLP_BASE_URL + 'search/author'

DBLP_PERSON_URL = DBLP_BASE_URL + 'pers/xk/{urlpt}'
DBLP_PUBLICATION_URL = DBLP_BASE_URL + 'rec/bibtex/{key}.xml'

class LazyAPIData(object):
	def __init__(self, lazy_attrs):
		self.lazy_attrs = set(lazy_attrs)
		self.data = None

	def __getattr__(self, key):
		if key in self.lazy_attrs:
			if self.data is None:
				self.load_data()
			return self.data[key]
		raise AttributeError, key

	def load_data(self):
		pass

class Author(LazyAPIData):
	"""
	Represents a DBLP author. All data but the author's key is lazily loaded.
	Fields that aren't provided by the underlying XML are None.
	Attributes:
	name - the author's primary name record
	publications - a list of lazy-loaded Publications results by this author
	homepages - a list of author homepage URLs
	homonyms - a list of author aliases
	"""
	def __init__(self, urlpt):
		self.urlpt = urlpt
		self.xml = None
		super(Author, self).__init__(['name','publications','homepages',
									  'homonyms'])

	def load_data(self):
		resp = requests.get(DBLP_PERSON_URL.format(urlpt=self.urlpt))
		# TODO error handling
		xml = resp.content
		self.xml = xml
		try: root = etree.fromstring(xml)
		except etree.XMLSyntaxError as e:
			try: root = etree.fromstring(xml)
			except etree.XMLSyntaxError as e:
				print "error again!"
				raise ValueError

		data = {
			'name':root.attrib['name'],
			'publications':[Publication(k) for k in 
							root.xpath('/dblpperson/dblpkey[not(@type)]/text()')],
			'homepages':root.xpath(
				'/dblpperson/dblpkey[@type="person record"]/text()'),
			'homonyms':root.xpath('/dblpperson/homonym/text()')
		}

		self.data = data

def first_or_none(seq):
	try:
		return next(iter(seq))
	except StopIteration:
		pass

Publisher = namedtuple('Publisher', ['name', 'href'])
Series = namedtuple('Series', ['text','href'])
Citation = namedtuple('Citation', ['reference','label'])

class Publication(LazyAPIData):
	"""
	Represents a DBLP publication- eg, article, inproceedings, etc. All data but
	the key is lazily loaded. Fields that aren't provided by the underlying XML
	are None.
	Attributes:
	type - the publication type, eg "article", "inproceedings", "proceedings",
	"incollection", "book", "phdthesis", "mastersthessis"
	sub_type - further type information, if provided- eg, "encyclopedia entry",
	"informal publication", "survey"
	title - the title of the work
	authors - a list of author names
	journal - the journal the work was published in, if applicable
	volume - the volume, if applicable
	number - the number, if applicable
	chapter - the chapter, if this work is part of a book or otherwise
	applicable
	pages - the page numbers of the work, if applicable
	isbn - the ISBN for works that have them
	ee - an ee URL
	crossref - a crossrel relative URL
	publisher - the publisher, returned as a (name, href) named tuple
	citations - a list of (text, label) named tuples representing cited works
	series - a (text, href) named tuple describing the containing series, if
	applicable
	"""
	def __init__(self, key):
		self.key = key
		self.xml = None
		super(Publication, self).__init__( ['type', 'sub_type', 'mdate',
				'authors', 'editors', 'title', 'year', 'month', 'journal',
				'volume', 'number', 'chapter', 'pages', 'ee', 'isbn', 'url',
				'booktitle', 'crossref', 'publisher', 'school', 'citations',
				'series'])

	def load_data(self):
		resp = requests.get(DBLP_PUBLICATION_URL.format(key=self.key))
		xml = resp.content
		self.xml = xml
		try: root = etree.fromstring(xml)
		except etree.XMLSyntaxError as e:
			try: root = etree.fromstring(xml)
			except etree.XMLSyntaxError as e:
				raise ValueError
		publication = first_or_none(root.xpath('/dblp/*[1]'))
		if publication is None:
			raise ValueError
		data = {
			'type':publication.tag,
			'sub_type':publication.attrib.get('publtype', None),
			'mdate':publication.attrib.get('mdate', None),
			'authors':publication.xpath('author/text()'),
			'editors':publication.xpath('editor/text()'),
			'title':first_or_none(publication.xpath('title/text()')),
			'year':int(first_or_none(publication.xpath('year/text()'))),
			'month':first_or_none(publication.xpath('month/text()')),
			'journal':first_or_none(publication.xpath('journal/text()')),
			'volume':first_or_none(publication.xpath('volume/text()')),
			'number':first_or_none(publication.xpath('number/text()')),
			'chapter':first_or_none(publication.xpath('chapter/text()')),
			'pages':first_or_none(publication.xpath('pages/text()')),
			'ee':first_or_none(publication.xpath('ee/text()')),
			'isbn':first_or_none(publication.xpath('isbn/text()')),
			'url':first_or_none(publication.xpath('url/text()')),
			'booktitle':first_or_none(publication.xpath('booktitle/text()')),
			'crossref':first_or_none(publication.xpath('crossref/text()')),
			'publisher':first_or_none(publication.xpath('publisher/text()')),
			'school':first_or_none(publication.xpath('school/text()')),
			'citations':[Citation(c.text, c.attrib.get('label',None))
						 for c in publication.xpath('cite') if c.text != '...'],
			'series':first_or_none(Series(s.text, s.attrib.get('href', None))
					  for s in publication.xpath('series'))
		}

		self.data = data

def dblp_search(author_str):
	resp = requests.get(DBLP_AUTHOR_SEARCH_URL, params={'xauthor':author_str})
	#TODO error handling
	try: root = etree.fromstring(resp.content)
	except etree.XMLSyntaxError as e:
		root = etree.fromstring(resp.content)
		raise ValueError
	return [Author(urlpt) for urlpt in root.xpath('/authors/author/@urlpt')]


import urllib2
import HTMLParser
import sys
import xml.dom.minidom as minidom
from htmlentitydefs import entitydefs
try:
	import xml.etree.cElementTree as ET
except ImportError:
	import xml.etree.ElementTree as ET
import glob
import os

reload(sys)
sys.setdefaultencoding('utf-8')
schools = ['ASU', 'Boston', 'CMU', 'Colorado', 'Dartmouth', 'Gatech', 'Indiana', 'MIT', 'NCSU', 'Rochester', 'RPI', 'Rutgers', 'Stanford', 
			'StonyBrook', 'TAMU', 'UArizona', 'UCB', 'UCDavis', 'UChicago', 'UCSB', 'UFL', 'UPitt', 'Utah', 'VirginiaTech', 'Wustl']
def search(ini_name):
	name = ini_name.strip()
	nname = name.split(',')
	errorflag = False
	if len(nname) > 1:
		name = nname[1] + ' ' + nname[0]
	else:
		pass
		
	try: authors = dblp_search(' ' + name + ' ')
	except ValueError:
		errorflag = True
	if errorflag:
		return (ini_name, -1)
	author_num = len(authors)

	if not authors:
		print "not found: " + name.encode('utf-8')
		sys.stdout.flush()
		return (ini_name, -1)
	else:
		if author_num > 10:
			print "multiple: " + str(author_num) + ' ' + name.encode('utf-8')
			sys.stdout.flush()

	cnt = 0
	index = 0
	if author_num > 1:
		for indx in range(author_num):
			try: 
				if authors[indx].name == name:
					break
			except ValueError:
				pass
			index += 1
		if index == len(authors):
			print "not found in the list!" + name + ' compare with ' + authors[0].name.encode('utf-8') + ' use default 0...'
			sys.stdout.flush()
			index = 0

	publications = authors[index].publications
	profname = authors[index].name
	for pub in publications:
		auth_len = len(pub.authors)
		pub_authors = []
		for i in range(auth_len):
			pub_authors.append(pub.authors[i])

		try: idx = pub_authors.index(profname)
		except ValueError:
			split_name = profname.split(' ')
			#profname = split_name[0] + ' ' + split_name[1][0] + '. ' + split_name[-1] #change middle name
			idx = 0
			for i in range(auth_len):
				pub_split = pub_authors[i].split(' ')
				if pub_split[0] == split_name[0] and pub_split[-1] == split_name[-1]:
					break
				idx += 1
				
			if idx == auth_len:
				print pub.title.encode('utf-8')
				sys.stdout.flush()
				#print pub.authors
				idx = -1

		if idx >= 0:
			cnt += 1.0 / (idx + 1)
	return (ini_name, cnt)


if __name__ == "__main__":
	for school in schools:
		print "=== start crawling school:" + school
		sys.stdout.flush()
		filename = school + '/' + school + '.xml'
		if not os.path.isfile(filename):
			print "cannot find: " + filename
			sys.stdout.flush()
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
					print school + ': ' + name.encode('utf-8') + ' with score: ' + "%.4f" % cnt
					sys.stdout.flush()
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
		sys.stdout.flush()

