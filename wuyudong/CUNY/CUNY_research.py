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

    def getGroupList(self, url):
        page = self.getPage(url)
        regex = '<span style="font-size:93%">(.*?)</span>'
        myItems = re.findall(regex, page.read(), re.S)
        regex = '<a.*?> <strong>(.*?)</strong></a>'
        # myItems = re.findall(regex, tmpStr, re.S)
        # print len(myItems)
        # print myItems
        # return
        for item in myItems:
            # print item
            # GroupName = item[0]
            # regex = '<a.*?>(.*?)</a>'
            myTokens = re.findall(regex, item, re.S)
            # print myTokens
            print "\t\t\t<professorname>%s</professorname>" % myTokens[0]
            # print myTokens
            # self.groups.append(Group(GroupName, myTokens))
            # print ProfName
            # print ProfPhotoUrl
            # print ProfPUrl
            # print ProfTitle
            # print ProfArea
            # print ProfOffice
            # print " "
            # self.profs.append(Prof(ProfName, ProfPhotoUrl, ProfPUrl, ProfTitle, ProfArea, ProfOffice))

    def outPutGroup(self):
        result = "<?xml version=\"1.0\" ?>\n\t<institution>\n"
        self.getGroupList()
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
        file = open("CUNY_research1.xml","w")
        file.writelines(result)



# baseURL = 'http://www.gc.cuny.edu/Page-Elements/Academics-Research-Centers-Initiatives/Doctoral-Programs/Computer-Science/Research-Areas/Algorithms'
# baseURL = 'http://www.gc.cuny.edu/Page-Elements/Academics-Research-Centers-Initiatives/Doctoral-Programs/Computer-Science/Research-Areas/Data-Science'
# baseURL = 'http://www.gc.cuny.edu/Page-Elements/Academics-Research-Centers-Initiatives/Doctoral-Programs/Computer-Science/Research-Areas/Artificial-Intelligence'
# baseURL = 'http://www.gc.cuny.edu/Page-Elements/Academics-Research-Centers-Initiatives/Doctoral-Programs/Computer-Science/Research-Areas/Communication-Networks-and-Computer-Systems'
# baseURL = 'http://www.gc.cuny.edu/Page-Elements/Academics-Research-Centers-Initiatives/Doctoral-Programs/Computer-Science/Research-Areas/Computational-Biology'
# baseURL = 'http://www.gc.cuny.edu/Page-Elements/Academics-Research-Centers-Initiatives/Doctoral-Programs/Computer-Science/Research-Areas/Computational-Science-and-Modeling'
# baseURL = 'http://www.gc.cuny.edu/Page-Elements/Academics-Research-Centers-Initiatives/Doctoral-Programs/Computer-Science/Research-Areas/Computer-and-Network-Security'
# baseURL = 'http://www.gc.cuny.edu/Page-Elements/Academics-Research-Centers-Initiatives/Doctoral-Programs/Computer-Science/Research-Areas/Logic'
# baseURL = 'http://www.gc.cuny.edu/Page-Elements/Academics-Research-Centers-Initiatives/Doctoral-Programs/Computer-Science/Research-Areas/Machine-Learning'
# baseURL = 'http://www.gc.cuny.edu/Page-Elements/Academics-Research-Centers-Initiatives/Doctoral-Programs/Computer-Science/Research-Areas/Natural-Language-Processing'
# baseURL = 'http://www.gc.cuny.edu/Page-Elements/Academics-Research-Centers-Initiatives/Doctoral-Programs/Computer-Science/Research-Areas/Signal-Image-Processing'
baseURL = 'http://www.gc.cuny.edu/Page-Elements/Academics-Research-Centers-Initiatives/Doctoral-Programs/Computer-Science/Research-Areas/Theory'
pl = GroupList(baseURL)
# pl.getPage()
# pl.outPutGroup()
pl.getGroupList(baseURL)
