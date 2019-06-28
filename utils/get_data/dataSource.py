# -*- coding:utf-8 -*-
"""
@author: ZHAO ZI RUI 14253801

This is the dataSource.py to crawler rawData and store it to MongoDB.
"""
import os

print('Crawling movie data from Douban...')
os.system('python douban_movie.py')
print('Douban Movie stored in MongoDB...')
    
print('Crawling movie data from IMDB...')
os.system('python imdb_movie.py')
print ('IMDB Movie stored in MongoDB...')
    
print('Crawling music data from Last.fm...')
os.system('python last_music.py')
print ('Last.fm Music stored in MongoDB...')
