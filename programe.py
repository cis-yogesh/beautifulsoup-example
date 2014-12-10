from GoogleScraper import search
import MySQLdb
from datetime import datetime


class GoogleScraperModel(object):
    """
        scrap google page according to given query and page number

        Search the given query string using Google.

        @type  query: str
        @param query: Query string. Must NOT be url-encoded.

        @type  tld: str
        @param tld: Top level domain.

        @type  lang: str
        @param lang: Languaje.

        @type  num: int
        @param num: Number of results per page.

        @type  start: int
        @param start: First result to retrieve.

        @type  stop: int
        @param stop: Last result to retrieve.
    
    """

    def __init__(self,query='', results_in_page=10, page=1, last_page=None, lang='en', tld='com',host="localhost",port=3306,user="root",password='123',db="google_scraper"):
        self.query = query
        self.page = page
        self.last_page = None
        self.lang = lang
        self.tld = tld
        self.results_in_page = results_in_page
        self.results = []

        if not last_page:
            self.last_page = page+1
        else:
            self.last_page = last_page*results_in_page
        try:
            self.db=MySQLdb.connect(host=host,port=port,user=user,passwd=password,db=db)
            self.cursor=self.db.cursor()
        except Exception as e:
            raise Exception('Database connection failed: {}'.format(e))

    def scrap(self):
        """get iterator object from search method and the inset result to database"""
        print self.query,self.results_in_page, self.page, self.last_page,self.lang
        self.results = search(self.query,num=self.results_in_page, start=self.page, stop=self.last_page,lang=self.lang)
        try:
            self.cursor.execute("""insert into search(search_string,date)values(%s,%s)""",(self.query,datetime.now()))
            self.db.commit()
            inserted_id = self.cursor.lastrowid
            print inserted_id
        except Exception as e:
            raise Exception('search query insert error: {}'.format(e))
        for url in self.results:
            self.cursor.execute("""insert into search_urls(search_id,url)values(%s,%s)""",(inserted_id,url))
        self.db.commit()
