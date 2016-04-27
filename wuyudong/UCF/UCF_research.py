__author__ = 'cutylewiwi'

# -*- coding:utf-8 -*-
import urllib
import urllib2
import re

class Group:
    def __init__(self, name, faculties):
        self.name = name
        self.faculties = faculties

class GroupList:

    def __init__(self, baseUrl):
        self.baseUrl = baseUrl
        self.groups = []

    def getPage(self, _url):
        try:
            url = _url
            request = urllib2.Request(url)
            response = urllib2.urlopen(request)
            # print response.read()
            return response
        except urllib2.URLError, e:
            if hasattr(e,"reason"):
                print u"Faild to get Prof List at University of Delaware",e.reason
                return None

    def getGroupList(self):
        page = self.getPage(self.baseUrl)
        # regex = '<p>.*?</p>\n<ul type="square">(.*?)</ul>'
        regex = '<span class="facultynames.*?">(.*?)</span>'
        myItems = re.findall(regex, page.read(), re.S)
        # print myItems
        # tmpStr = myItems[0]
        # regex = '<li>.*?<em>(.*?)</em>(.*?)</li>'
        # myItems = re.findall(regex, tmpStr, re.S)
        # del myItems[0]
        # del myItems[0]
        # print len(myItems)
        # print myItems
        # return
        print "\t\t<research>"
        print "\t\t\t<groupname></groupname>"
        for item in myItems:
            print "\t\t\t<professorname>%s</professorname>" % item
            # print item
            # GroupName = ""
            # regex = '<li>(.*?) \(<a'
            # GroupFaculties = re.findall(regex, item, re.S)
            # print GroupFaculties
            # self.groups.append(Group(GroupName, GroupFaculties))
            # print ProfName
            # print ProfPhotoUrl
            # print ProfPUrl
            # print ProfTitle
            # print ProfArea
            # print ProfOffice
            # print " "
            # self.groups.append(Prof(ProfName, ProfPhotoUrl, ProfPUrl, ProfTitle, ProfArea, ProfOffice))
        print "\t\t</research>\n"

    def outPutProf(self):
        result = "<?xml version=\"1.0\" ?>\n\t<institution>\n"
        self.getGroupList()
        return
        for group in self.groups:
            result += "\t\t<research>\n"
            result += "\t\t\t<groupname>%s</groupname>\n" % (group.name)
            for faculty in group.faculties:
                tmpStr = faculty
                if tmpStr[:3] == "Dr.":
                    tmpStr = tmpStr[4:]
                result += "\t\t\t<professorname>%s</professorname>\n" % (tmpStr)
            result += "\t\t</research>\n"
        result += "\t</institution>\n"
        # print result
        file = open("UCF_research.xml","w")
        file.writelines(result)




baseURL = 'http://www.cs.ucf.edu/research/crcv.php'
baseURL = 'http://www.cs.ucf.edu/research/ip.php'
baseURL = 'http://www.cs.ucf.edu/research/mlai.php'
baseURL = 'http://www.cs.ucf.edu/research/vrhci.php'
baseURL = 'http://www.cs.ucf.edu/research/graphics.php'
baseURL = 'http://www.cs.ucf.edu/research/ses.php'
baseURL = 'http://www.cs.ucf.edu/research/db.php'
baseURL = 'http://www.cs.ucf.edu/research/pc.php'
baseURL = 'http://www.cs.ucf.edu/research/nmc.php'
baseURL = 'http://www.cs.ucf.edu/research/csdf.php'
baseURL = 'http://www.cs.ucf.edu/research/bsb.php'
baseURL = 'http://www.cs.ucf.edu/research/tcaqc.php'
baseURL = 'http://www.cs.ucf.edu/research/ca.php'
pl = GroupList(baseURL)
# pl.getPage()
pl.outPutProf()
# pl.getGroupList()
