import pandas as pd

#import data
path = 'part2_dataset_1.csv'
#path=encode("utf-8").strip()
sms = pd.read_csv(path, header=None,names=['create_time','user_id','user_name','message','label'])
#the original data set is not balanced so i did a undersampling here 
sa = pd.read_csv('Sleep_annotation.csv', delimiter=",", header=None,names=['user_id','message','label'])

#examine the shape
sms.shape

X_1 = sa.message
X_2 = sms.message
Y_1 = sa.label
Y_2 = sms.label
amount_1 = sa.message.count()
amount_2 = sms.message.count()

#import the keyword list 
key_terms = open('sleep.txt','r')
for s in range( 0,amount_2):
	if not any(key_term in sms.message.loc[s] for key_term in key_terms):
		sms.label.loc[s]=-1
	else:
		sms.label.loc[s]=1

#split x and y into training and testing sets
#from sklearn.cross_validation import train_test_split
#X_train, X_test,Y_train,Y_test = train_test_split(X_1,Y_1, random_state = 4)

#use annotated data as the training data 
X_train = X_1
X_test  = sms.message
Y_train = Y_1
Y_test  = sms.label
#print(Y_train.value_counts())
#print(Y_test.value_counts())
##print(Y_test.get_values())

#instantiate the vectorizer, apply a stopword dictionary and delete the  high frequency and low frequency words 
from sklearn.feature_extraction.text import CountVectorizer
vect = CountVectorizer(stop_words='english',max_df=0.95,min_df=2)

#from sklearn.feature_extraction.text import TfidfVectorizer
#vect = TfidfVectorizer(stop_words='english',max_df=0.95,min_df=1)

#learning the vocabulary of the training data and then create a document term matrix
#vect.fit(X_train)
#X_train_dtm = vect.transform(X_train)
X_train_dtm = vect.fit_transform(X_train)
#transfer the testing data into a document term matrix
X_test_dtm = vect.transform(X_test)


#LogisticRegression
from sklearn.linear_model import LogisticRegression
logreg = LogisticRegression()
#train the model with the x train dtm
logreg.fit(X_train_dtm, Y_train)
#make prediction
y_pre_class = logreg.predict(X_test_dtm)
#make a confusion matrix
from sklearn import metrics
print "LogisticRegression"
print metrics.confusion_matrix(Y_test,y_pre_class)
print metrics.accuracy_score(Y_test,y_pre_class)



#print  X_test[y_pre_class == 1].get_values()
