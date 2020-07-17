import pymongo
import json
import requests
from instagram import get_page_data_instagram
from fbdata import get_page_data
from twitter import get_page_data_twitter
from pymongo import MongoClient
import random
import socket
import fbdata
from nltk.corpus import wordnet
from nltk import word_tokenize
from collections import Counter
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
english_stopwords=stopwords.words('english')
from nltk import ngrams

from Tkinter import *
import tkMessageBox as tm
import os

class LoginFrame(Frame):
	
	def facebook():
		global num_posts
		num_posts=fbdata.count * 25
		cursor = db.fb.find()
		w1=0.1
		w2=0.2
		w3=0.7
		sum=0	
		for document in cursor:
			fan_count=document['fan_count']
			talking_about_count=document['talking_about_count']
		#for a in document['posts']['data']:
		#	num_posts+=1
		sum=w1*fan_count+w2*talking_about_count+w3*num_posts
		return sum

	def facebook_keyword(self):  
		stemmed=PorterStemmer()
		all_tokens=[]
		all_tokens_stemmed=[]
		all_bigrams = []
		keywords=" "
		cursor = db.fb.find()
		for document in cursor:
			page_id=document['id']
		url='https://graph.facebook.com/v2.12/'+str(page_id)+'/posts?limit=15&access_token='+access_token
		data2=requests.get(url)
		response=json.loads(data2.text)
		#print response
		for post in response['data']:
			if 'message' in post:
				tokens=word_tokenize(post['message'].encode('utf-8').lower())
				#stemmed_tokens=stemmed.stem(tokens)				
				bigrams=list(ngrams(tokens,3))	
				#print bigrams
				all_tokens=all_tokens+tokens
				all_bigrams=all_bigrams+bigrams
		#print all_tokens
		#for token in all_tokens:
		#	stemmed_tokens=stemmed.stem(token)
		#	all_tokens_stemmed.append(stemmed_tokens)

		frequencies=Counter(all_bigrams)
		for token,count in frequencies.most_common(25):
			flag=0
			for x in token:
				if x in english_stopwords or len(x)<2:
					flag=1
					break	
			if flag==0:                        
				fstr=','.join(token)
				keywords=keywords+"("+fstr+")"+" "+str(count)+"\n"
			else:
				continue
		
		labelfont3 = ('times', 20, 'bold','italic')
		labelfont4 = ('times', 15, 'bold','italic')
		
		self.label_3=Label(self, text="Facebook", bg="darkblue", fg="white", height=3,width=20,justify="center",font=labelfont3)

		self.label_4=Label(self, text="URL:  https://www.facebook.com/"+self.entry_1.get(), bg="black", fg="white", height=3,width=40,justify="center",font=labelfont4)
		
		self.label_3.grid(row=4,sticky=NW,column=1,pady=4)
		self.label_4.grid(row=5,sticky=NW,column=1,pady=4)

		tm.askokcancel( "Keyword Recommendation",keywords)


	def twitter():
		num_posts=0
		w1=0.1
		w2=0.2
		w3=0.7
		sum=0
		cursor = db.twitter.find()
		for document in cursor:
			if num_posts==0: 
		  	#print document['text']
	          	#print document['favorite_count']
	          	#print document['retweeted']
	          	#print document['retweet_count']
		  	#print document['user']['verified'] #user is verified or not
		  	#print document['user']['followers_count']
		  	#print document['user']['friends_count']
		  	#print document['user']['description']
		  	#print document['user']['statuses_count']
		  	#print document['user']['favourites_count']
				sum=w1*document['user']['followers_count']+w2*document['user']['statuses_count']+\
				w3*document['user']['favourites_count']
				num_posts=num+posts+1
		return sum

	def twitter_keyword(self):
		stemmed=PorterStemmer()
		all_tokens=[]
		all_tokens_stemmed=[]
		all_bigrams = []
		keywords=" "
		cursor = db.twitter.find()
		for post in cursor:
			if 'text' in post:
				#print post['text']
				tokens=word_tokenize(post['text'].encode('utf-8').lower())
				bigrams=list(ngrams(tokens,2))	
				all_tokens=all_tokens+tokens
				all_bigrams=all_bigrams+bigrams

		for token in all_tokens:
			stemmed_tokens=stemmed.stem(token)
			all_tokens_stemmed.append(stemmed_tokens)
		
		frequencies=Counter(all_bigrams)
		for token,count in frequencies.most_common(25):
			flag=0
			for x in token:
				if x in english_stopwords or len(x)<2:
					flag=1
					break	
			if flag==0:                        
				fstr=','.join(token)
				keywords=keywords+"("+fstr+")"+" "+str(count)+"\n"
			else:
				continue
		
		labelfont5 = ('times', 20, 'bold','italic')
		labelfont6 = ('times', 15, 'bold','italic')
		
		self.label_5=Label(self, text="Twitter", bg="darkblue", fg="white", height=3,width=20,justify="center",font=labelfont3)

		self.label_6=Label(self, text="URL:  https://twitter.com/"+self.entry_1.get(), bg="black", fg="white", height=3,width=40,justify="center",font=labelfont4)
		
		self.label_5.grid(row=4,sticky=NW,column=1,pady=4)
		self.label_6.grid(row=5,sticky=NW,column=1,pady=4)

		tm.askokcancel( "Keyword Recommendation", keywords)

	def __init__(self, master):
		global fbcount
		global tweet

		Frame.__init__(self,master)
		labelfont0=('helvetica','30','bold')
		labelfont= ('times', 15, 'bold')
		
		self.label_0=Label(self, text="SM RECOMMENDATION PORTAL",
font=labelfont0,bg="peachpuff",fg="black")
		self.label_1 = Label(self, text="Topic",font=labelfont)
		self.label_2 = Label(self, text="Content Type",font=labelfont)

		self.entry_1 = Entry(self)
		self.entry_2 = Entry(self)	

		self.label_0.grid(row=0,column=1)		
		self.label_1.grid(row=1,sticky=E)
		self.label_2.grid(row=2, sticky=E)		

		self.entry_1.grid(row=1, column=1)
		self.entry_2.grid(row=2, column=1)

		if self.entry_2.get()=='text' or self.entry_2.get()=='Text':
			get_page_data()
			get_page_data_twitter(self.entry_1.get())
			fbcount=facebook()
			tweet=twitter
		score=max(fbcount,tweet)

		if score==fbcount:
			self.logbtn = Button(self, text="Show", command = self.facebook_keyword,bg="darkgrey",fg="black")
		else:
			self.logbtn = Button(self, text="Show", command = self.twitter_keyword,fg="black",bg="darkgrey")

		self.logbtn.grid(columnspan=2)
		self.pack()

access_token='EAACEdEose0cBAKok8VPGZADFZBql4332h8hDVySwYNZAzFGeepK0NDOJhuVNBtXDOnnpu54KDoYc94gvsTDfVJou3ZATrFMzJTzL3u159XP8I9D2mLRrnnA1Cpbsi1qUltfLppyZCgvOOTGIg3G7Rldzecpf11B658Bac3UERBbGmtSoOL3m29fGbQ406wkZB3QIf39NUT1gZDZD'
client = MongoClient('localhost:27017')
db=client.major   
flag=1
fbcount=0
tweet=0
num_posts=0
root=Tk()
lf=LoginFrame(root)
root.mainloop()	
