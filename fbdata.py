import requests
import json
import pymongo
from pymongo import MongoClient
response={}
count=0
page_id="ipl"
access_token='EAACEdEose0cBAKok8VPGZADFZBql4332h8hDVySwYNZAzFGeepK0NDOJhuVNBtXDOnnpu54KDoYc94gvsTDfVJou3ZATrFMzJTzL3u159XP8I9D2mLRrnnA1Cpbsi1qUltfLppyZCgvOOTGIg3G7Rldzecpf11B658Bac3UERBbGmtSoOL3m29fGbQ406wkZB3QIf39NUT1gZDZD'
connection=MongoClient()
db=connection['major']	
def get_page_data():
	global response
	global count
	flag=0
	url='https://graph.facebook.com/v2.12/'+str(page_id)+'?fields=description,posts{message},category,fan_count,talking_about_count,verification_status,name&access_token='+access_token
	data2=requests.get(url)
	response=json.loads(data2.text)
	db['fb'].remove({})
	db['fb'].insert(response)
	while(1):
		if flag==1:
			break	
		try:
			if count==0:
				url=response['posts']['paging']['next']
				count=count+1
			else:
				#print "next page"
				data2=requests.get(url)
				response=json.loads(data2.text)
				url=response['paging']['next']
				#print "dhingra"
				count=count+1
				print count
		except KeyError:		
			pass
			flag=1
	
	
#get_page_id('school')

