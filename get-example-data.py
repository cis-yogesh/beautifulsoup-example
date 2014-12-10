from bs4 import BeautifulSoup
from selenium import webdriver
#http://3fnhfsfc2bpzdste.onion/index.php?a=download&q=1329

class ScrapeMethod():

    def __init__(self):
        self.SetDriver()
        self.AllContentList = []

    def SetDriver(self):
        self.driver = webdriver.Firefox()

    def GetAlldata(self, url):
        self.driver.get(url)
        pagesource = self.driver.page_source
        soup = BeautifulSoup(pagesource)
        return soup

    def Pastebin(self):
        url = 'http://pastebin.ca'
        soupData = self.GetAlldata(url)
        recentPost = soupData.find(id="idmenurecent").find_all("a")
        allLinks = []
        for recent in recentPost:
            allLinks.append(url + recent.attrs['href'])
        return allLinks

    def Quickleak(self):
        url = 'https://www.quickleak.org/last-pastes.html'
        puturl = '/'.join(url.split('/')[:-1])
        soupData = self.GetAlldata(url)
        table = soupData.find("table", {"id": "example"})
        allLinks = []
        for row in table.findAll("tr"):
            if row.td:
                link = row.td.find('a').attrs['href']
                allLinks.append(puturl + '/' + link)
        return allLinks

    def CloseDriver(self):
        self.driver.close()

    def AllLinks(self):
        self.AllLinksList = self.Pastebin() + self.Quickleak()
        return 'self.Quickleak() + self.Pastebin()'

    def ContentData(self):
        self.AllLinks()
        for content in self.AllLinksList:
            soupData = self.GetAlldata(content)

            if 'pastebin' in content:
                self.PastebinContent(content, soupData)

            if 'quickleak' in content:
                self.QuickleakContent(content, soupData)
        return self.AllContentList

    def PastebinContent(self, url, getData):

        contentdata = getData.select("div > #idsec0 > .ccontent li")
        headingdata = getData.select("div #idsec0 h2 dt")

        tempDict = {
            'url': url,
            'heading': self.GetString(headingdata),
            'content': self.GetString(contentdata),
        }

        self.AllContentList.append(tempDict)

    def QuickleakContent(self, url, getData):

        contentdata = getData.select("div > .content li")
        headingdata = getData.select("div .page-title .titlebar h2")

        tempDict = {
            'url': url,
            'heading': self.GetString(headingdata),
            'content': self.GetString(contentdata),
        }

        self.AllContentList.append(tempDict)

    def GetString(self, contentdata):
        string = ''
        for content in contentdata:
            txt = content.text
            string = string + txt + '\n '
        return string

ScrapeObject = ScrapeMethod()
print ScrapeObject.ContentData()
