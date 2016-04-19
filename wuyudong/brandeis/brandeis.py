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
        pageString = page.read()
        # end = re.search("Instructors and Visiting Faculty", page.read())
        # endIndex = end.start()
        # regex = '<tr>.*?<td.*?<img.*?src=\"(.*?)\".*?<td.*?<p.*?<a href=\"(.*?)\".*?><strong>(.*?)(<br />)?</strong>.*?</a>.*?<br />(.*?)<br />(.*?)<br />(.*?)<br /><a.*?>(.*?)</a>.*?</td>.*?<td.*?<p>(.*?)</p>.*?</td>.*?</tr>'
        regex = r'<tr>.*?<td valign="top">.*?<a.*?>.*?<strong>([^<].*?)(<br />\n)?</strong>.*?</a>.*?</td>.*?</tr>'
        myItems = re.findall(regex, pageString, re.S)
        regex = r'<tr>.*?<td valign="top">.*?<strong>.*?<a.*?>(.*?)</a>.*?</strong>.*?</td>.*?</tr>'
        myItems += re.findall(regex, pageString, re.S)
        print myItems
        for item in myItems:
            print item[0]
            print item[1]
        return
        for item in myItems:
            ProfName = item[2]
            ProfPhotoUrl = "http://www.brandeis.edu/programs/computerscience/" + item[0]
            ProfPUrl = item[1]
            ProfTitle = ""#item[3]
            ProfArea = ""#item[7]
            ProfOffice = ""#item[4]
            ProfPhone = ""#item[5]
            ProfEmail = ""#item[6]
            print ProfName
            print ProfPhotoUrl
            print ProfPUrl
            print ProfTitle
            print ProfArea
            print ProfOffice
            print ProfPhone
            print ProfEmail
            print " "
            self.profs.append(Prof(ProfName, ProfPhotoUrl, ProfPUrl, ProfTitle, ProfArea, ProfOffice, ProfPhone, ProfEmail))

    def outPutProf(self):
        result = "<?xml version=\"1.0\" ?>\n\t<institution>\n"
        self.getProfList()
        for prof in self.profs:
            result += "\t\t<professor>\n"
            result += "\t\t\t<name>%s</name>\n" % (prof.name)
            result += "\t\t\t<title>%s</title>\n" % (prof.title)
            result += "\t\t\t<office>%s</office>\n" % (prof.office)
            result += "\t\t\t<email>%s</email>\n" % (prof.phone)
            result += "\t\t\t<phone>%s</phone>\n" % (prof.email)
            result += "\t\t\t<website>%s<website>\n" % (prof.pUrl)
            result += "\t\t\t<image>%s<\image>\n" % (prof.photoUrl)
            result += "\t\t</professor>\n"
        result += "\t</institution>\n"
        # print result
        file = open("result/brandeis.txt","w")
        file.writelines(result)




baseURL = 'http://www.brandeis.edu/programs/computerscience/cs-faculty.html'
pl = ProfList(baseURL)
# pl.outPutProf()
pl.getProfList()
# pl.getPage()
