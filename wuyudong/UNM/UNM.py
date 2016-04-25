__author__ = 'cutylewiwi'

# -*- coding:utf-8 -*-
import urllib
import urllib2
import re

class Prof:
    def __init__(self, name, photoUrl, pUrl, title, area, office, phone, email):
        self.name = name
        self.photoUrl = photoUrl
        self.pUrl = pUrl
        self.title = title
        self.area = area
        self.office = office
        self.phone = phone
        self.email = email

class ProfList:

    def __init__(self, baseUrl):
        self.baseUrl = baseUrl
        self.profs = []

    def getPage(self):
        try:
            url = self.baseUrl
            request = urllib2.Request(url)
            response = urllib2.urlopen(request)
            # print response.read()
            return response
        except urllib2.URLError, e:
            if hasattr(e,"reason"):
                print u"Faild to get Prof List at University of Delaware",e.reason
                return None

    def getProfList(self):
        page = self.getPage()
        # regex = '<div class=\"wdn-grid-set\">.*?<a class=\"wdn-button\" title=\"Web page for.*?\" href=\"(.*?)\".*?<strong>(.*?)</strong>.*?<div class=\"gs-fac-rsch\">(.*?)(<br />)?</div>'
        regex = '<div class="single-person-entry computer-science">(.*?)</div>'
        myItems = re.findall(regex, page.read(), re.S)
        # print myItems[0]
        # return
        for item in myItems:
            tmpStr = item
            regex = '<h4><a href="(.*?)">(.*?)</a>'
            myTokens = re.findall(regex, tmpStr, re.S)
            ProfName = myTokens[0][1]
            ProfPUrl = "http://www.cs.unm.edu/directory/" + myTokens[0][0]
            regex = '<img.*?src="(.*?)".*?>'
            myTokens = re.findall(regex, tmpStr, re.S)
            ProfPhotoUrl = "http://www.cs.unm.edu/directory/" + myTokens[0]
            regex = '<span class="personlist-title">(.*?)</span></h4>'
            myTokens = re.findall(regex, tmpStr, re.S)
            ProfTitle = myTokens[0]
            ProfArea = ""
            regex = '<tr><td>Office: </td><td>(.*?)</td></tr>'
            myTokens = re.findall(regex, tmpStr, re.S)
            ProfOffice = myTokens[0][6:]
            regex = '<tr><td>Phone: </td><td>(.*?)</td></tr>'
            myTokens = re.findall(regex, tmpStr, re.S)
            ProfPhone = myTokens[0][6:]
            regex = '<tr><td>Email: </td><td>.*?<a href="mailto:(.*?)">.*?</a></td></tr>'
            myTokens = re.findall(regex, tmpStr, re.S)
            ProfEmail = myTokens[0]
            # print ProfName
            # print ProfPhotoUrl
            # print ProfPUrl
            # print ProfTitle
            # print ProfArea
            # print ProfOffice
            # print ProfPhone
            # print ProfEmail
            # print " "
            self.profs.append(Prof(ProfName, ProfPhotoUrl, ProfPUrl, ProfTitle, ProfArea, ProfOffice, ProfPhone, ProfEmail))

    def outPutProf(self):
        result = "<?xml version=\"1.0\" ?>\n\t<institution>\n"
        self.getProfList()
        for prof in self.profs:
            result += "\t\t<professor>\n"
            result += "\t\t\t<name>%s</name>\n" % (prof.name)
            result += "\t\t\t<title>%s</title>\n" % (prof.title)
            result += "\t\t\t<office>%s</office>\n" % (prof.office)
            result += "\t\t\t<email>%s</email>\n" % (prof.email)
            result += "\t\t\t<phone>%s</phone>\n" % (prof.phone)
            result += "\t\t\t<website>%s</website>\n" % (prof.pUrl)
            result += "\t\t\t<image>%s</image>\n" % (prof.photoUrl)
            result += "\t\t</professor>\n"
        result += "\t</institution>\n"
        # print result
        fileName = "UNM.xml"
        outputDir = "result"
        file = open(fileName,"w")
        file.writelines(result)




baseURL = 'http://www.cs.unm.edu/directory/index.html'
pl = ProfList(baseURL)
pl.outPutProf()
# pl.getPage()
# pl.getProfList()
