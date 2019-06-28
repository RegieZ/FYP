#!coding:utf-8
"""
@author: ZHAO ZI RUI 14253801

This is the last_music.py to crawl rawData from Last.fm Music.
"""
import requests
import time
import urllib3

urllib3.disable_warnings()
from bs4 import BeautifulSoup
from pymongo import MongoClient

headers = {'Accept': 'text/html, */*; q=0.01',
           'accept-encoding': 'gzip, deflate, br',
           'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
           'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1'}


def getHtml():
    global url
    for ch in range(0x41, 0x5B):
        url = 'https://www.last.fm/search/tracks?q={0}'.format(chr(ch))
        res = requests.get(url, headers=headers, verify=False)
        res.encoding = 'utf-8'
        yield res.text


def listeners(musicUrl):
    Listeners = ''
    try:
        res = requests.get('https://www.last.fm' + musicUrl, headers=headers, verify=False)
        res.encoding = 'utf-8'
        soup = BeautifulSoup(res.text, 'lxml')
        Listeners = soup.find('abbr')['title']
    except:
        pass
    return Listeners


def parse(soup):
    global n
    client = MongoClient('mongodb://127.0.0.1:27017')
    db = client.lastdb
    lastData = db.lastData
    for i in soup.find_all(class_='js-link-block'):
        try:
            data = i.find_all(class_='chartlist-name')[0]
            Name = data.text.strip().replace('\n', '').split('—')[1]
            Author = data.text.strip().replace('\n', '').split('—')[0]
            url = data.find_all('a')[-1]['href']
            Comments = listeners(url)
            if not Name or not Author or not Comments:
                continue
            n += 1
            print(n)
            result = lastData.insert_one(
                {'Name':Name,'Author':Author,'Comments':Comments}
            )
            print(result.inserted_id)
            print(u'Name: %s\nAuthor: %s\nComments: %s\n' % (Name, Author, Comments))
            time.sleep(2)
        except Exception as e:
            print(e)
            continue

n = 0
html = getHtml()
for i in html:
    soup = BeautifulSoup(i, 'lxml')
    parse(soup)
