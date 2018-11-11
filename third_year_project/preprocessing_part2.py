import json
import re
import pandas as pd

#data_file = open('../project/new.json','r')

data_file = ('odd_tweets_1.csv')
sms = pd.read_csv(data_file,names=['user_name','user_id','create_time','message'])#, delimiter=",", header=None,names=['user_name','user_id','create_time','message'])
#print sms.message.head(10)
count = sms.message.count()-1
#emoji_pattern = re.compile("["
#	u"\U0001F600-\U0001F64F" #emoticons
#	u"\U0001F300-\U0001F5FF" #sysbols & pictographs
#	u"\U0001F680-\U0001F6FF" #transport & map symbol
#	u"\U0001F1E0-\U0001F1FF" #flags(ios)
#	u"\U00002700-\U000027B0" #Dingbats
#	u"\U000024C2-\U0001F:251" #Enclosed characters
#	u"\U0001F30D-\U0001F567" 
#	u"\U0001F600-\U0001F999"
#	u"\U00002000-\U00002700"
#	u"\xa0"
#	"]+",flags=re.UNICODE)
#emoji_pattern = re.compile('\S')
mention_pattern = re.compile('\#')#('\#\S+[\s|$]')
hashtag_pattern = re.compile('\@\S+\s|$')


for i in range(0,count):
	sms.message.loc[i] = re.sub(r'http\S+','',sms.message.loc[i])#remove url
	sms.message.loc[i] = re.sub(r'\n','',sms.message.loc[i])#remove \n
	sms.message.loc[i] = re.sub(r',',' ',sms.message.loc[i])#remove \n
	sms.message.loc[i] = re.sub(r'"',' ',sms.message.loc[i])#remove \n
	sms.message.loc[i] = mention_pattern.sub(r'',sms.message.loc[i])#remove @username
	sms.message.loc[i] = re.sub(r'&amp','',sms.message.loc[i])#remove retweet
	sms.message.loc[i] = hashtag_pattern.sub(r'',sms.message.loc[i])#remove hashtag
	#sms.message.loc[i] = emoji_pattern.sub(r'',sms.message.loc[i])#remove emoji
	sms.message.loc[i] = re.sub(r'RT','',sms.message.loc[i])#remove \n
	if ((sms.message.loc[i].isspace() != True) and (sms.message.loc[i] != "") and (sms.message.loc[i]!=".")):
		if re.search(r'^\s[\sa-zA-Z0-9]+',sms.message.loc[i])!=None:	
			print sms.create_time.loc[i],",",sms.user_id.loc[i],",",sms.user_name.loc[i],",",sms.message.loc[i],","
	 

