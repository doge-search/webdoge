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
        # pageString = page.read()
        #regex = r'<tr>.*?<td valign="top">.*?<a.*?>.*?<strong>([^<].*?)(<br />\n)?</strong>.*?</a>.*?</td>.*?</tr>'
        regex = '<table align="left" border="0" cellpadding="6" cellspacing="8" class="table-590">.*?<tbody>(.*?)<h4>Instructors and Visiting Faculty</h4>'
        myItems = re.findall(regex, page.read(), re.S)
        #regex = r'<tr>.*?<td valign="top">.*?<strong>.*?<a.*?>(.*?)</a>.*?</strong>.*?</td>.*?</tr>'
        #myItems += re.findall(regex, pageString, re.S)
        tmpStr = myItems[0]
        regex = '<tr>(.*?)</tr>'
        myItems = re.findall(regex, tmpStr, re.S)
        # print myItems
        # for item in myItems:
            # print item[0]
            # print item[1]
        # return
        for item in myItems:
            regex = '<td.*?>.*?<img.*?src="(.*?)".*?>.*?</td>.*?<td.*?>.*?</td>.*?<td.*?>.*?</td>'
            tmpStr = item
            myTokens = re.findall(regex, tmpStr, re.S)
            if len(myTokens) > 0:
                ProfPhotoUrl = "http://www.brandeis.edu/programs/computerscience/" + myTokens[0]
            print myTokens
            regex = '<td.*?>.*?</td>.*?<td.*?>.*?<a href="(.*?)".*?>(<strong>)?(.*?)(</strong>)?</a>.*?</td>.*?<td.*?>.*?</td>'
            myTokens = re.findall(regex, tmpStr, re.S)
            print myTokens
            if len(myTokens) > 0:
                ProfName = ""
                # ProfPhotoUrl = "http://www.brandeis.edu/programs/computerscience/"
                ProfPUrl = ""
                ProfTitle = ""#item[3]
                ProfArea = ""#item[7]
                ProfOffice = ""#item[4]
                ProfPhone = ""#item[5]
                ProfEmail = ""#item[6]
            # print ProfName
            # print ProfPhotoUrl
            # print ProfPUrl
            # print ProfTitle
            # print ProfArea
            # print ProfOffice
            # print ProfPhone
            # print ProfEmail
            # print " "
            if ProfName != "":
                self.profs.append(Prof(ProfName, ProfPhotoUrl, ProfPUrl, ProfTitle, ProfArea, ProfOffice, ProfPhone, ProfEmail))

    def outPutProf(self):
        result = "<?xml version=\"1.0\" ?>\n\t<institution>\n"
        # self.getProfList()
        self.profs.append(Prof("", "", "", "", "", "", "", ""))
        for prof in self.profs:
            result += "\t\t<professor>\n"
            result += "\t\t\t<name>%s</name>\n" % (prof.name)
            result += "\t\t\t<title>%s</title>\n" % (prof.title)
            result += "\t\t\t<office>%s</office>\n" % (prof.office)
            result += "\t\t\t<email>%s</email>\n" % (prof.phone)
            result += "\t\t\t<phone>%s</phone>\n" % (prof.email)
            result += "\t\t\t<website>%s</website>\n" % (prof.pUrl)
            result += "\t\t\t<image>%s</image>\n" % (prof.photoUrl)
            result += "\t\t</professor>\n"
        result += "\t</institution>\n"
        # print result
        file = open("brandeis.xml","w")
        file.writelines(result)




baseURL = 'http://www.brandeis.edu/programs/computerscience/cs-faculty.html'
pl = ProfList(baseURL)
pl.outPutProf()
# pl.getProfList()
# pl.getPage()
