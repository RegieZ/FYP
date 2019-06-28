#!coding:utf-8
"""
@author: ZHAO ZI RUI 14253801

This is the imdb_movie.py to crawl rawData from IMDB Most Popular Movie.
"""
import requests
import time
import urllib3

urllib3.disable_warnings()
from bs4 import BeautifulSoup
from pymongo import MongoClient

headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
           'accept-encoding': 'gzip, deflate, br',
           'Host': 'm.imdb.com',
           'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1'}


def getHtml():
    url = 'https://m.imdb.com/chart/moviemeter?ref_=m_nv_mv_mvm'
    res = requests.get(url, headers=headers, verify=False)
    res.encoding = 'utf-8'
    return res.text


def getAuthor(Url):
    Author = ''
    try:
        res = requests.get('https://m.imdb.com' + Url, headers=headers, verify=False)
        res.encoding = 'utf-8'
        soup = BeautifulSoup(res.text, 'lxml')
        Author = soup.find("a", attrs={"itemprop": "director"}).find('span').text.replace('\n', '')
    except:
        pass
    return Author


def parse(soup):
    global n
    client = MongoClient('mongodb://127.0.0.1:27017')
    db = client.imdbdb
    imdbData = db.imdbData
    for i in soup.find_all(class_='media'):
        try:
            Name = i.find('h4').text.replace('\n', ' ')
            url = i.find('a')['href']
            Score = i.find(class_='imdb-rating').text
            Author = getAuthor(url)
            if not Name or not Author or not Score:
                continue
            n += 1
            print(n)
            result = imdbData.insert_one(
                {'Name':Name,'Author':Author,'Score':Score}
            )
            print(result.inserted_id)
            print(u'Name: %s\nAuthor: %s\nScore: %s\n' % (Name, Author, Score))
            time.sleep(2)
        except Exception as e:
            continue


n = 0
html = getHtml()
soup = BeautifulSoup(html, 'lxml')
parse(soup)
