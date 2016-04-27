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
        regex = '<div class="span-19 last" style="margin-bottom:5px;">.*?<img src="(.*?)".*?<div class="span-7 facultyInfoPanel">.*?<h3 style="margin:0px;">(.*?)</h3>.*?<span style="font-size:11px;">(.*?)</span>(.*?)</div>.*?<div class="span-9 last">(.*?)</div>\n</div>'
        #regex = '<tr>.*?<img src=\"(.*?)\".*?</tr>'
        myItems = re.findall(regex, page.read(), re.S)
        # print myItems
        # return
        for item in myItems:
            ProfName = item[1]
            ProfPhotoUrl = "http://www.eecs.ku.edu" + item[0]
            ProfPUrl = ""
            ProfTitle = item[2]
            ProfArea = ""
            ProfOffice = ""
            ProfPhone = ""
            ProfEmail = ""
            interestRe = r'<li>(.*?)</li>'
            interests = re.findall(interestRe, item[4], re.S)
            for interest in interests:
                ProfArea += interest + ", "
            if len(interests) > 0:
                ProfArea = ProfArea[:-2]

            profileRe = r'<li class="email"><a.*?>(.*?)</a></li>'
            profileObj = re.findall(profileRe, item[3], re.S)
            if len(profileObj) > 0:
                ProfEmail = profileObj[0]

            profileRe = r'<li class="phone">(.*?)</li>'
            profileObj = re.findall(profileRe, item[3], re.S)
            if len(profileObj) > 0:
                ProfPhone = profileObj[0]

            profileRe = r'<li class="website"><a href="(.*?)".*?</a></li>'
            profileObj = re.findall(profileRe, item[3], re.S)
            if len(profileObj) > 0:
                ProfPUrl = profileObj[0]

            profileRe = r'<li class="office"><a.*?>(.*?)</a></li>'
            profileObj = re.findall(profileRe, item[3], re.S)
            if len(profileObj) > 0:
                ProfOffice = profileObj[0]
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
        fileName = "KU.xml"
        outputDir = "result"
        file = open(fileName,"w")
        file.writelines(result)




baseURL = 'http://www.eecs.ku.edu/people/faculty'
pl = ProfList(baseURL)
pl.outPutProf()
# pl.getPage()
# pl.getProfList()
