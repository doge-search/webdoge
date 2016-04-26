import os 
import xml.dom.minidom as minidom

def Test1(rootDir): 
	list_dirs = os.walk(rootDir) 
	for root, dirs, files in list_dirs: 
		for fname in files: 
			if(fname.endswith('.prof')):
				print 'doing ' + fname
				fprefix = fname[:-5]
				if(not os.path.exists('d:/PYPJ/webdoge/hehao/' + fprefix)):
					os.mkdir('d:/PYPJ/webdoge/hehao/' + fprefix)
				fout_xml = file('d:/PYPJ/webdoge/hehao/' + fprefix + '/' + fprefix + '.xml','w')
				doc = minidom.Document()
				institution = doc.createElement("institution")
				doc.appendChild(institution)
				with open(fname,'r') as fin:
					for line in fin.readlines():
						prof = doc.createElement("professor")
						profname = doc.createElement("name")
						institution.appendChild(prof)
						prof.appendChild(profname)
						profname.appendChild(doc.createTextNode(line[:-1]))
						# print line
				doc.writexml(fout_xml, "\t", "\t", "\n")
				fout_xml.close()
				# return
Test1('D:\PYPJ\webdoge\hehao')