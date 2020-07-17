import json
from twython import Twython
import sys
import pymongo
from pymongo import MongoClient
reload(sys)
sys.setdefaultencoding('utf-8')

APP_KEY='dVYRfPM8pdlZ3VtOF9mlTbzHY'
APP_SECRET='dNj6wlirBrPtj1BxSbVAoxiwhCkhP7oKsp132aFGLK6msgE7z0'
OAUTH_TOKEN='222097362-Mg4qI0zJW6KszcCukvVzAKopTnLIuCMrnIXPBen9'
OAUTH_TOKEN_SECRET='pJc8M9WvrImTdXb8f78VSFL4x1lpaGLHPQZK7MbUxpnyD'

twitter=Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

connection =MongoClient()
db=connection['major']	

case_list =[]

def get_page_data_twitter(page_name):
	data=twitter.search(q=page_name,result_type='mixed',count=2)
	statuses=data['statuses']
	#print statuses
	db['twitter'].remove({})
	db['twitter'].insert(statuses)
	
#get_page_data_twitter('ipl')


