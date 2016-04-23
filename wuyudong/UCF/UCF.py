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
        regex = '<div class="faculty three columns end">.*?<img.*?src="(.*?)".*?>.*?<span class="facultynames.*?">(.*?)</span>.*?<span class="nobold">(.*?)</span>.*?</div>'
        # regex = '<div class="faculty three columns end">(.*?)</div>'
        myItems = re.findall(regex, page.read(), re.S)
        # print len(myItems)
        # print myItems
        # return
        for item in myItems:
            ProfName = item[1]
            ProfPhotoUrl = "http://www.cs.ucf.edu/people/" + item[0]
            ProfPUrl = ""
            ProfTitle = item[2]
            ProfArea = ""
            ProfOffice = ""
            ProfPhone = ""
            ProfEmail = ""
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
        fileName = "UCF.xml"
        outputDir = "result"
        file = open(fileName,"w")
        file.writelines(result)




baseURL = 'http://www.cs.ucf.edu/people/index.php'
pl = ProfList(baseURL)
# pl.outPutProf()
# pl.getPage()
pl.getProfList()
