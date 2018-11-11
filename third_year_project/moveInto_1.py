from pymongo import MongoClient
import json
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import datetime

# The MongoDB connection info. This assumes your database name is TwitterStream, and your collection name is tweets.
client = MongoClient()
db = client.TwitterStream
#db.tweets.ensure_index("id", unique=True, dropDups=True)
collection = db.tweet_6

# Add the keywords you want to track. They can be cashtags, hashtags, or words.
keywords = ["Asleep and never wake", 
	"Just want to sleep forever",
	"Take my own life", 
	"End it all",
	"My life isn't worth",
	"Want to be dead",
	"End my life",
	"Not want to be alive",
	"Want to be gone",
	"End this pain",
	"Nothing to live for",
	"Ending it all",
	"Point in living",
	"Want to die",
	"Put an end to this",
	"Want to disappear",
	"Ready to die",
	"Want to end it",
	"I'm drowning",
	"Really need to die",
	"Wanted to die",
	"Stop the pain",
	"Wanting to kill yourself and",
	"Suicidal",
	"Isn't worth living",
	"Suicide",
	"Why should I continue living",
	"Tired of living",
	"Leave this world",
	"Wanna die",
	"Want to die",
	"Deserve to die",
	"Desire to end my life",
	"Tried suicide",
	"Commit suicide",
	"Committing suicide",
	"Feeling suicidal",
	"Shoot myself",
	"A gun to head",
	"Hang myself",
	"Hurt myself",
	"Cut myself"]

# Optional - Only grab tweets of specific language
language = ['en']

# You need to replace these with your own values that you get after creating an app on Twitter's developer portal.
access_token = "3854934923-V2mzUpyTHgpbzEUwaVh2sEIn0QpsLwGIOhUDZBu"
access_token_secret = "qzaGkfmDG2VJweZ1zekdUUhDleIjFdpfY9aF89QNCEzcH"
consumer_key = "YKFwh5ZKl3ZdzLQ26bGJ4yJqi"
consumer_secret = "1I0rigWuuwfdwKL4uVTgC2sAyWa36Fhv0FCeJIIEd5TFd1Uqgm"


# The below code will get Tweets from the stream and store only the important fields to your database
class StdOutListener(StreamListener):

    def on_data(self, data):

        # Load the Tweet into the variable "t"
        t = json.loads(data)

        # Pull important data from the tweet to store in the database.
        tweet_id = t['id_str']  # The Tweet ID from Twitter in string format
        username = t['user']['screen_name']  # The username of the Tweet author
        text = t['text']  # The entire body of the Tweet     
        dt = t['created_at']  # The timestamp of when the Tweet was created


        # Convert the timestamp string given by Twitter to a date object called "created". This is more easily manipulated in MongoDB.
        created = datetime.datetime.strptime(dt, '%a %b %d %H:%M:%S +0000 %Y')

        # Load all of the extracted Tweet data into the variable "tweet" that will be stored into the database
        tweet = {'id':tweet_id, 'username':username,'text':text, 'created':created}

        # Save the refined Tweet data to MongoDB
 	#print tweet

    	collection.save(tweet)
        # Optional - Print the username and text of each Tweet to your console in realtime as they are pulled from the stream
        #print username + ':' + ' ' + text
        return True

    # Prints the reason for an error to your console
    def on_error(self, status):

        print status 

# Some Tweepy code that can be left alone. It pulls from variables at the top of the script
if __name__ == '__main__':
	try:
		l = StdOutListener()
		auth = OAuthHandler(consumer_key, consumer_secret)
		auth.set_access_token(access_token, access_token_secret)
		stream = Stream(auth, l)
	except KeyError:
		pass
	except:
		pass
stream.filter(track=keywords, languages=language)
