import os
import xml.dom.minidom as minidom

school = 'MSU'
if(not os.path.exists('d:/PYPJ/webdoge/hehao/' + school)):
    os.mkdir('d:/PYPJ/webdoge/hehao/' + school)

# for line in open('d:/PYPJ/webdoge/hehao/' + school + '.html'):  

fout_xml = file('d:/PYPJ/webdoge/hehao/' + school + '/' + school + '_research.xml','w')
doc = minidom.Document()
institution = doc.createElement("institution")
doc.appendChild(institution)
cnt = 0
ccc = 0
group = 'n'
for line in open('d:/PYPJ/webdoge/hehao/' + school + '.html'):
	if(group == 'n'):
		group = 'y'
		research = doc.createElement("research")
		groupname = doc.createElement("groupname")
		institution.appendChild(research)
		research.appendChild(groupname)
		groupname.appendChild(doc.createTextNode(line[:-1]))
	else:
		if(len(line)==1):
			cnt += 1
			group = 'n'
		else:
			professorname = doc.createElement("professorname")
			research.appendChild(professorname)
			professorname.appendChild(doc.createTextNode(line[:-1]))

# print cnt, ccc
doc.writexml(fout_xml, "\t", "\t", "\n")
fout_xml.close()