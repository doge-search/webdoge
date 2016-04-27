__author__ = 'cutylewiwi'

# -*- coding:utf-8 -*-
import urllib
import urllib2
import re

class Prof:
    def __init__(self, name, photoUrl, pUrl, title, area, office):
        self.name = name
        self.photoUrl = photoUrl
        self.pUrl = pUrl
        self.title = title
        self.area = area
        self.office = office

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
        #regex = '<div class=\"one-third column\">.*?<li>(.*?)</li>.*?</div>'
        regex = '<div class="one-third column clear">.*?<h2>Full-Time</h2>.*?<ul>(.*?)</ul>.*?</div>'
        #regex = '<tr>.*?<img src=\"(.*?)\".*?</tr>'
        myItems = re.findall(regex, page.read(), re.S)
        tmpStr = myItems[0]
        # print tmpStr
        regex = '<li>.*?<a.*?href="(.*?)">(.*?)</a>.*?</li>'
        myItems = re.findall(regex, tmpStr, re.S)
        # print myItems
        # return
        for item in myItems:
            # print item
            ProfName = item[1]
            ProfPhotoUrl = ""
            ProfPUrl = "http://www.eecs.utk.edu/people/faculty" + item[0]
            ProfTitle = ""
            ProfArea = ""
            ProfOffice = ""
            # print ProfName
            # print ProfPhotoUrl
            # print ProfPUrl
            # print ProfTitle
            # print ProfArea
            # print ProfOffice
            # print " "
            self.profs.append(Prof(ProfName, ProfPhotoUrl, ProfPUrl, ProfTitle, ProfArea, ProfOffice))

    def outPutProf(self):
        result = "<?xml version=\"1.0\" ?>\n\t<institution>\n"
        self.getProfList()
        for prof in self.profs:
            result += "\t\t<professor>\n"
            result += "\t\t\t<name>%s</name>\n" % (prof.name)
            result += "\t\t\t<title>%s</title>\n" % (prof.title)
            result += "\t\t\t<office>%s</office>\n" % (prof.office)
            result += "\t\t\t<email></email>\n"
            result += "\t\t\t<phone></phone>\n"
            result += "\t\t\t<website>%s</website>\n" % (prof.pUrl)
            result += "\t\t\t<image>%s</image>\n" % (prof.photoUrl)
            result += "\t\t</professor>\n"
        result += "\t</institution>\n"
        # print result
        file = open("UTK.xml","w")
        file.writelines(result)




baseURL = 'http://www.eecs.utk.edu/people/faculty/'
pl = ProfList(baseURL)
# pl.getPage()
pl.outPutProf()
# pl.getProfList()
