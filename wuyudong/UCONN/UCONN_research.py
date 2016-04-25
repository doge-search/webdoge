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
        regex = '<h4>(.*?)</h4>\n<ul>(.*?)</ul>'
        myItems = re.findall(regex, page.read(), re.S)
        # print len(myItems)
        # print myItems
        # return
        for item in myItems:
            # print item
            GroupName = item[0]
            regex = '<a.*?>(.*?)</a>'
            GroupFaculties = re.findall(regex, item[1], re.S)
            self.groups.append(Group(GroupName, GroupFaculties))
            # print ProfName
            # print ProfPhotoUrl
            # print ProfPUrl
            # print ProfTitle
            # print ProfArea
            # print ProfOffice
            # print " "
            # self.profs.append(Prof(ProfName, ProfPhotoUrl, ProfPUrl, ProfTitle, ProfArea, ProfOffice))

    def outPutProf(self):
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
        file = open("UCONN_research.xml","w")
        file.writelines(result)




baseURL = 'https://www.cse.uconn.edu/research/research-map/'
pl = GroupList(baseURL)
# pl.getPage()
pl.outPutProf()
# pl.getGroupList()
