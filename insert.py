import pymongo
import json
import requests
import csv
import fbdata
from pymongo import MongoClient
from datetime import datetime

def facebook():
    global fb_nop
    global fb_followers
    global fb_shares
    cursor = db.fb.find()
    for document in cursor:
          fb_followers=document['fan_count']
          fb_shares=document['talking_about_count']
    fbdata.get_page_data()
    fb_nop=fbdata.count*25
    


def twitter():
    num_posts=0
    global t_followers
    global t_shares
    global t_nop
    cursor = db.twitter.find()
    for document in cursor:
	  if num_posts==0: 
	  	t_followers=document['user']['followers_count']
	  	t_nop=document['user']['statuses_count']
	  	t_shares=document['user']['favourites_count']
	  num_posts+=1
    
fb_nop=0
t_nop=0
fb_followers=0
t_followers=0
fb_shares=0
t_shares=0   

if __name__ == '__main__':
    client = MongoClient('localhost:27017')
    db=client.major
    facebook()
    twitter()
    #print fb_followers
    #print fb_shares
    #print fb_nop
    #print t_followers
    #print t_shares
    #print t_nop
    with open('test.csv', 'a') as newFile:
    	newFileWriter = csv.writer(newFile)
    	newFileWriter.writerow([datetime.now(),fb_followers,fb_shares,fb_nop,t_followers,t_shares,t_nop])
    fbscore=0.1*fb_followers+0.2*fb_shares+0.7*fb_nop
    tscore=0.1*t_followers+0.2*t_shares+0.7*t_nop
    if fbscore >= tscore:
    	output=1
    else:
    	output=0
    with open('fbipl.csv', 'a') as newFile:
    	newFileWriter = csv.writer(newFile)
    	newFileWriter.writerow([fb_followers,fb_shares,fb_nop,output])
    with open('tipl.csv', 'a') as newFile:
    	newFileWriter = csv.writer(newFile)
    	newFileWriter.writerow([t_followers,t_shares,t_nop,output])
    


