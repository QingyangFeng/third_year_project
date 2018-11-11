import pandas as pd
import spacy
import math
import re
from spacy.symbols import nsubj, VERB

nlp = spacy.load('en')
#import database
path = 'part1_dataSet.csv'
#path=encode("utf-8").strip()
sms = pd.read_csv(path, delimiter=",", header=None,names=['create_time','user_id','user_name','message','label'])
#import annotated data, but i did a little bit undersampling due to the data set is not balanced
sa = pd.read_csv('Suicide_annotation.csv', delimiter=",", header=None,names=['create_time','user_id','user_name','message','label'])
#examine the shape
sms.shape

#define x,y with countvectorizer
X_1 = sa.message
X_2 = sms.message
Y_1 = sa.label
Y_2 = sms.label
amount_1 = sa.message.count()-1
amount_2 = sms.message.count()-1

n=0

doc = nlp(unicode(sms.message.tail(amount_2)))
#reset the label of all the 
for s in range( 0,amount_2):
	sms.label.loc[s]=0

#verb before pronoun
#reset n
n=0
i=amount_2/float(700)
i=math.ceil(i)
i=int(i)
#verbs_1 = []
for h in range(1,i):
	for possible_verb in doc:
		if possible_verb.pos==VERB :
			if possible_verb.lemma_==unicode("die") or possible_verb.lemma_==unicode("want") or possible_verb.lemma_==unicode("wanna") or possible_verb.lemma_==unicode("kill") or possible_verb.lemma_==unicode("end") or possible_verb.lemma_==unicode("suicide") or possible_verb.lemma_==unicode("hate") or possible_verb.lemma_==unicode("take") or possible_verb.lemma_==unicode("hurt") or possible_verb.lemma_==unicode("feel") or possible_verb.lemma_==unicode("hang") or possible_verb.lemma_==unicode("shoot") or possible_verb.lemma_==unicode("tired") or possible_verb.lemma_==unicode("shoot") or possible_verb.lemma_==unicode("cut"):
				sms.label.loc[amount_2-n]=1
				if possible_verb.tag_!= unicode("VBD") and possible_verb.tag_!=("VBP") :
					for possible_subject in possible_verb.children:
						if possible_subject.dep==nsubj and (possible_subject.lemma_==unicode("i") or possible_subject.lemma_==unicode("myself")  or possible_subject.lemma_==unicode("my")):
							sms.label.loc[amount_2-n]=3
				elif possible_verb.tag_==unicode("VBP") or possible_verb.lemma_==unicode("want") or possible_verb.lemma_==unicode("wanna") :	
					for possible_subject in possible_verb.children:						
						if possible_subject.dep==nsubj and (possible_subject.lemma_==unicode("i") or possible_subject.lemma_==unicode("myself")  or possible_subject.lemma_==unicode("my")):						
							sms.label.loc[amount_2-n]=2
				elif possible_verb.tag_==unicode("VBD") :
					for possible_subject in possible_verb.children:
						if possible_subject.dep==nsubj and (possible_subject.lemma_==unicode("i") or possible_subject.lemma_==unicode("myself")  or possible_subject.lemma_==unicode("my")):						
							sms.label.loc[amount_2-n]=1
			else:
				sms.label.loc[amount_2-n] = 0
		else:
			sms.label.loc[amount_2-n] = 0		
		n=n+1

#print sms.label.value_counts()
#reset n 

#verb after pronoun
n=0
for h in range(1,i):
	for possible_subject in doc:
		if sms.label.loc[amount_2-n]== 0 or sms.label.loc[amount_2-n]==float("nan") :
			if possible_subject.dep == nsubj and (possible_subject.lemma_==unicode("i")  or possible_subject.lemma_==unicode("myself")  or possible_subject.lemma_==unicode("my")) :
				if possible_subject.head.pos==VERB: 
					if possible_subject.head.lemma_==unicode("die") or possible_subject.head.lemma_==unicode("want") or possible_subject.head.lemma_==unicode("wanna") or possible_subject.head.lemma_==unicode("kill") or possible_subject.head.lemma_==unicode("end") or possible_subject.head.lemma_==unicode("suicide") or possible_subject.head.lemma_==unicode("hate") or possible_subject.head.lemma_==unicode("take") or possible_subject.head.lemma_==unicode("hurt") or possible_subject.head.lemma_==unicode("feel") or possible_subject.head.lemma_==unicode("hang") or possible_subject.head.lemma_==unicode("shoot") or possible_subject.head.lemma_==unicode("tired") or possible_subject.head.lemma_==unicode("shoot") or possible_subject.head.lemma_==unicode("cut"):#("kill" or "end" or "die" or "hate" or "take" or "hurt" or "feel" or "hang" or "suicide" or "tired" or "cut" or "decide" or "shoot"):
				#print 3.2
						if possible_subject.head.tag_ !=unicode("VBD") and possible_subject.head.tag_ !=("VBP"):
#		verbs.add(possible_subject.head)
					#print 3.3					
							sms.label.loc[amount_2-n]=3							
				#else:
				#	print 3.4
				#	sms.label.loc[amount_2-n]=0
						elif possible_subject.head.tag_==unicode("VBP") or possible_subject.head.lemma_==unicode("want") or possible_verb.lemma_==unicode("wanna"):
					#print 3.5				
							sms.label.loc[amount_2-n]=2					
						elif possible_subject.head.tag_==unicode("VBD"):
				#print 3.6
							sms.label.loc[amount_2-n]=1
				else:	
					sms.label.loc[amount_2-n] = 0
			else:
				sms.label.loc[amount_2-n] = 0	
		n=n+1

#some specific situation
for x in range(0,amount_2):
	if re.search(r'(\i|\I)[\s]*(\want|\wanna|\WANNA|\WANT)',sms.message.loc[x])!=None:
		sms.label.loc[x]=2
	elif re.search(r'(\news|\hotline|\youtube|\BBC|\blast|\Squad|\Bomb|\crminal)',sms.message.loc[x])!=None:
		sms.label.loc[x]=0
	elif re.search(r'\work|\homework|\music|\shows',sms.message.loc[x])!=None:
		sms.label.loc[x]=1
	elif re.search(r'\ready|\Ready',sms.message.loc[x])!=None:
		sms.label.loc[x]=2

#print sms.label.value_counts()
#split x and y into training and testing sets
#from sklearn.cross_validation import train_test_split
#X_train, X_test,Y_train,Y_test = train_test_split(X,Y, random_state = 4

#use annotated dataset as training data
X_train = X_1
X_test  = sms.message
Y_train = Y_1
Y_test  = sms.label

#print (X_train.shape)
#print (X_train.dtype)
#print(X_test.shape)
#print(Y_train.get_values())
#print(Y_test.get_values())

#Kfold
#from sklearn.model_selection import KFold
#kf = KFold(n_splits = 5)
#for train_index, test_index in kf.split(X):
#	X_train, X_test = X[train_index], X[test_index]
#	Y_train, Y_test = Y[train_index], Y[test_index]

#instantiate the vectorizer
#from sklearn.feature_extraction.text import CountVectorizer
#vect = CountVectorizer()

#term-frequency tfidf
from sklearn.feature_extraction.text import TfidfVectorizer
vect = TfidfVectorizer(stop_words='english',min_df=1)
#vect.fit(X_train)
#X_train_dtm = vect.transform(X_train)

#learning the vocabulary of the training data and then create a document term matrix
X_train_dtm = vect.fit_transform(X_train)
#transfer the testing data into a document term matrix
X_test_dtm = vect.transform(X_test)

#print X_test_dtm
#print X_train_dtm

#MultinomialNB
from sklearn.naive_bayes import MultinomialNB
nb = MultinomialNB()
#train the model with X_train_dtm
nb.fit(X_train_dtm,Y_train)
y_pred_class = nb.predict(X_test_dtm)
#Y_test = y_pred_class
from sklearn import metrics

print metrics.confusion_matrix(Y_test,y_pred_class)
print "MultinomialNB"
print metrics.accuracy_score(Y_test,y_pred_class)

#LogisticRegression
from sklearn.linear_model import LogisticRegression
logreg = LogisticRegression()
logreg.fit(X_train_dtm, Y_train)
y_pre_class = logreg.predict(X_test_dtm)
#print y_pre_class
print metrics.confusion_matrix(Y_test,y_pre_class)
print "LogisticRegression"
print metrics.accuracy_score(Y_test,y_pre_class)


#calculate the number of different labels
a_0= X_train[Y_train == 0].count() + X_test[y_pred_class == 0].count()
a_1= X_train[Y_train == 1].count() + X_test[y_pred_class == 1].count()
a_2= X_train[Y_train == 2].count() + X_test[y_pred_class == 2].count()
a_3= X_train[Y_train == 3].count() + X_test[y_pred_class == 3].count()


print "the percentage of positive tweet: ", a_3/float(amount_2+amount_1+2)*100 , "%"
print "the percentage of positive and potential positive tweet: ", (a_3+a_2)/float(amount_2+amount_1+2)*100 , "%"
print "the percentage of potential positive tweet: ", a_2/float(amount_2+amount_1+2)*100 , "%"
print "the percentage of potential negative tweet: ", a_1/float(amount_2+amount_1+2)*100 , "%"
print "the percentage of potential negative and potential positive tweet: ", (a_2 + a_1)/float(amount_2+amount_1+2)*100 , "%"

#print X_test[y_pred_class == 2]
f = open('timeline_tweets_info.csv', 'w') 

#print out the positive tweets
for x in range(0,amount_1):
	if sa.label.loc[x]==3:
		if sa.user_id.loc[x]!=float('nan') and sa.user_name.loc[x]!=float('nan'):
			f.write(str(int(sa.user_id.loc[x])))
			f.write(",")
			f.write(sa.user_name.loc[x])
			f.write("\n")
#print  sms.label.value_counts()
#print  X_train[Y_train == 3].get_values(),"\n"
#print  X_test[y_pred_class == 0].get_values()
#print y_pred_class.shape

f.close()
