import tweepy
import time

#Twitter API goodies hehe
CONSUMER_KEY = 'ckey'
CONSUMER_SECRET = 'csecret'
ACCESS_KEY = 'akey'
ACCESS_SECRET = 'as'

#Possible useful methods: API.search() [under Help Methods]

#URL to reply with
URL = 'http://qm.ee/222C7062'
#file from which we grab ID's
FILE_NAME = 'last_seen_id.txt'

#Setting up the API
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

#search for tweets about needing money
twts_about_money = api.search(q = "Need money")

#list of strings to check for in tweets
spec_strings = ['need money',
	'Need Money',
	'Need money']

def retrieve_last_seen_id(file_name):
	f_read = open(file_name, 'r')
	last_seen_id = int(f_read.read().strip())
	f_read.close()
	return last_seen_id

def store_last_seen_id(last_seen_id, file_name):
	f_write = open(file_name, 'w')
	f_write.write(str(last_seen_id))
	f_write.close()
	return

#reply to tweets @ me with link
def reply_to_tweets_at_me():
	last_seen_id = retrieve_last_seen_id(FILE_NAME)
	mentions = api.mentions_timeline(last_seen_id, tweet_mode='extended')
	print('replying...')
	for mention in reversed(mentions):
		last_seen_id = mention.id
		store_last_seen_id(last_seen_id, FILE_NAME)
		if '#needmoney' in mention.full_text.lower():
			api.update_status('@' + mention.user.screen_name + 
				' Check out this free survey site on which I have been making $200 a week on! ' + URL,
				 mention.id)

#reply with link to people tweeting about needing money
def reply_with_links():
	for t in twts_about_money:
		print('responding...')
		api.update_status('@' + t.user.screen_name + 
			' Check out this free survey site on which I have been making $200 a week on! ' + URL,
				t.id)
		time.sleep(60)

while True:
	reply_with_links()
	#reply_to_tweets_at_me()	
