# -*- coding:utf-8 -*-
"""
@author: ZHAO ZI RUI 14253801

This is the process.py.
"""
import math
def readlines_song(filename):
    filejson = open(filename, 'r')
    keys = []
    s = json.load(filejson)
    for line in s['nodes']:
        dics = {}
        dics["Name"] = line['name']
        dics["Author"] = line['artist']
        dics["Comments"] = line['playcount']
        keys.append(dics)
    filejson.close()
    return keys

# Get Similarity Index
def Similar(Name, Author, Comment, filename):
    keys = readlines_song(filename)
    sim_score = []
    for line in keys:
        name = line["Name"]
        author = line["Author"]
        comment = int(line["Comments"])
        maxComment = 100000.0
        if Name == name:
            sim1 = 1
        else:
            sim1 = 0
        if Author == author:
            sim2 = 1
        else:
            sim2 = 0

        sim3 = math.sqrt(abs(int(Comment) - comment)/maxComment)
        sim = (0.6*sim1 + 0.3*sim2 + 0.1*sim3)/(sim1 + sim2 + sim3)
        sim_score.append(sim)
    return sim_score, keys

#ID Assignment
def id_for(rawData):   
    id = [rawData["name"], rawData["author"]].join("_")
    return id

# Link Creation
def link_for(Name, Author, Comment, filename):
    keys = readlines_song(filename)
    for line in keys:
        name = line[Name]
        author = line[Author]
        comment = int(line[Comment])
        if Similar(name, author, comment, filename).sim_score >= 0.15:
            return keys
        
# Second-Layer Link Creation
def links_for(Name, Author, Comment, filename):
    keys = link_for(Name, Author, Comment, filename)
    for line in keys:
        name = line["Name"]
        author = line["Author"]
        comment = int(line["Comments"])
        if Similar(name, author, comment, filename).sim_score >= 0.15:
            return keys

import json
if __name__ == '__main__':
    filename = './test.json'
    dic = {}
    filejson = open(filename, 'r')
    s = json.load(filejson)
    song = input("Please enter the song number: ")
    s_nodes = s['nodes'][int(song)]
    s_links = s['links']

    Name = s_nodes['name']
    Author = s_nodes['artist']
    Comment = s_nodes['playcount']

    dic['Name'] = Name
    dic["Author"] = Author
    dic["Comments"] = Comment

    sims, songs = Similar(dic["Name"], dic["Author"], dic["Comments"], filename)
    print("The Song list", songs)
    print("The Song similarity list", sims)

