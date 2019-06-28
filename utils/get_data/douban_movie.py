#!coding:utf-8
"""
@author: ZHAO ZI RUI 14253801

This is the douban_movie.py to crawl rawData from douban Movie Top250.
"""
import urllib3
import requests
import time


urllib3.disable_warnings()
from bs4 import BeautifulSoup
import re
from pymongo import MongoClient

def getHtml():
    headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
               'Host': 'movie.douban.com',
               'Referer': 'https://movie.douban.com/top250',
               'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1'}
    for pageIndex in range(10):
        url = 'https://movie.douban.com/top250?start=%d&filter=' % (pageIndex * 25)
        res = requests.get(url, headers=headers, verify=False)
        res.encoding = 'utf-8'
        yield res.text

def deleteChinese(oldS):
    return re.sub('[^a-zA-Z0-9\/]', '', oldS)

def parse(soup):
    global n
    client = MongoClient('mongodb://127.0.0.1:27017')
    db = client.doubandb
    doubanData = db.doubanData
    for i in soup.find_all(id='content')[0].find_all(class_="item"):
        try:
            Name = deleteChinese(i.find_all(class_='info')[0].find_all(class_='title')[1].text[3:].strip())
            Author = deleteChinese(' '.join(
                i.find_all(class_='info')[0].find('p').text.strip().split('\xa0')[0].replace('\xc2', '').split(' ')[2:]).strip())
            Comments = deleteChinese(i.find_all(class_='info')[0].find_all(class_='star')[0].find_all('span')[
                                         -1].text.strip())
            if not Name or not Author or not Comments:
                continue
            n += 1
            print(n)
            result = doubanData.insert_one(
                {'Name':Name,'Author':Author,'Comments':Comments}
            )
            print(result.inserted_id)
            print(u'Name: %s\nAuthor: %s\nComments: %s\n' % (Name, Author, Comments))
        except Exception as e:
            print(e)
            continue

n = 0
html = getHtml()
for i in html:
    time.sleep(5)
    soup = BeautifulSoup(i, 'lxml')
    parse(soup)
