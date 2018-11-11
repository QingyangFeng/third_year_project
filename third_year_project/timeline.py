import tweepy 
import csv
import pandas as pd
#Twitter API credentials
access_token = "3854934923-V2mzUpyTHgpbzEUwaVh2sEIn0QpsLwGIOhUDZBu"
access_token_secret = "qzaGkfmDG2VJweZ1zekdUUhDleIjFdpfY9aF89QNCEzcH"
consumer_key = "YKFwh5ZKl3ZdzLQ26bGJ4yJqi"
consumer_secret = "1I0rigWuuwfdwKL4uVTgC2sAyWa36Fhv0FCeJIIEd5TFd1Uqgm"

f = open('odd_tweets_1.csv', 'wb') 


def get_all_tweets(screen_name, since_id):
	#Twitter only allows access to a users most recent 3240 tweets with this method
	#print since_id
	#authorize twitter, initialize tweepy
	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_token_secret)
	api = tweepy.API(auth)
	
	#initialize a list to hold all the tweepy Tweets
	alltweets = []	
	
	#make initial request for most recent tweets (200 is the maximum allowed count)
	new_tweets = api.user_timeline(screen_name = screen_name, since_id = since_id,count=200)
	
	#save most recent tweets
	alltweets.extend(new_tweets)
	
	#save the id of the oldest tweet less one
	#oldest = alltweets[-1].id - 1
	
	#keep grabbing tweets until there are no tweets left to grab
	#while len(new_tweets) > 0:
	print "getting tweets before %s" % (since_id)
		
	#all subsiquent requests use the max_id param to prevent duplicates
	#new_tweets = api.user_timeline(screen_name = screen_name,count=200,max_id=oldest)
		
	#save most recent tweets
	#alltweets.extend(new_tweets)
		
	#update the id of the oldest tweet less one
	#oldest = alltweets[-1].id - 1
		
	#	print "...%s tweets downloaded so far" % (len(alltweets))
	
	#transform the tweepy tweets into a 2D array that will populate the csv	
	outtweets = [[tweet.user.screen_name,tweet.id_str, tweet.created_at, tweet.text.encode("utf-8")] for tweet in alltweets]
	
	#write the csv	
	writer = csv.writer(f)
	writer.writerows(outtweets)
	

	
	pass


if __name__ == '__main__':
	try:#pass in the username of the account you want to download
		path = open('timeline_tweets_info.csv','r')
		sms = pd.read_csv(path, delimiter=",", header=None,names=['user_id','user_name'])
		count = sms.user_id.count()-1
		#print sms.user_id.loc[1]
		for x in range(0,count):
			get_all_tweets(sms.user_name.loc[x],int(sms.user_id.loc[x]))

	except tweepy.error.TweepError:
		pass
