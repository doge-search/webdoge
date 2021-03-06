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
        regex = '<div class="row">.*?<img src="(.*?)".*?<div class="col-xs-8 col-sm-9 col-md-9 col-lg-10 person">.*?<a href="(.*?)".*?><h4>(.*?) - <i>(.*?)</i></h4></a>.*?<p><span class="glyphicons glyphicons-envelope"></span>(.*?)</p>.*?<p><span class="glyphicon glyphicon-phone-alt"></span>(.*?)</p>.*?<p><span class="glyphicons glyphicons-google-maps"></span>(.*?)</p>.*?</div>.*?</div>'
        # regex = '<div class="row">.*?<img src="(.*?)".*?<div class="col-xs-8 col-sm-9 col-md-9 col-lg-10 person">.*?<a href="(.*?)".*?><h4>(.*?) - <i>(.*?)</i></h4></a>.*?</div>.*?</div>'
        myItems = re.findall(regex, page.read(), re.S)
        # print myItems
        # return
        for item in myItems:
            ProfName = item[2]
            ProfPhotoUrl = "http://eng.auburn.edu" + item[0][5:]
            ProfPUrl = item[1]
            ProfTitle = item[3]
            ProfArea = ""
            ProfOffice = item[6][4:]
            ProfPhone = item[5][4:]
            ProfEmail = item[4][4:]
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
        fileName = "AUNURN.xml"
        file = open(fileName,"w")
        file.writelines(result)




baseURL = 'http://eng.auburn.edu/csse/faculty/index.html'
pl = ProfList(baseURL)
pl.outPutProf()
# pl.getPage()
# pl.getProfList()
