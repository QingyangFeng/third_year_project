import json
import re
data = [] 

#data_file = open('../project/new.json','r')

data_file = open('rawdataSet.json', 'r')
i=0
n=1
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
bad_words = ['squad',
	'RT',
	'bomb',	
	'attack',
	'blast',
	'he']

for line in data_file:
	data.append(json.loads(line))

	data[i]['text'] = re.sub(r'http\S+','',data[i]['text'])#remove url
	data[i]['text'] = re.sub(r'\n','',data[i]['text'])#remove \n
	data[i]['text'] = re.sub(r',',' ',data[i]['text'])#remove \n
	data[i]['text'] = re.sub(r'"',' ',data[i]['text'])#remove \n
	data[i]['text'] = mention_pattern.sub(r'',data[i]['text'])#remove @username
	data[i]['text'] = re.sub(r'&amp','',data[i]['text'])#remove retweet
	data[i]['text'] = hashtag_pattern.sub(r'',data[i]['text'])#remove hashtag
#	data[i]['text'] = emoji_pattern.sub(r'',data[i]['text'])#remove emoji
	if not any(bad_word in data[i]['text'] for bad_word in bad_words):	
		print data[i]['created'],",",data[i]['id'],",",data[i]['username'] ,",",u''.join(data[i]['text'],).encode("utf-8").strip()#, '-$-' +  data[i]['id']#remove obivous noice
		n=n+1
#		print data[i]
	i=i+1

		 

