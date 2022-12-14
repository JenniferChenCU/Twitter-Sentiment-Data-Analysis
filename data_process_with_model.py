# -*- coding: utf-8 -*-
"""Applied ML Data_Viewing.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1RP2Imcw0FRJTLIGcrpjISvSNsAfRrjeR
"""

import pandas as pd
import numpy as np

from google.colab import drive
drive.mount('/content/drive')

cd 'drive/My Drive/Applied Machine Learning'

ls

sentimental_df = pd.read_csv('training.1600000.processed.noemoticon.csv',engine ='python',header=None)
sentimental_df.columns = ['target','ids','date','flag','user','text']
sentimental_df.head()

sentimental_df['target'].value_counts()

#encode target variable
sentimental_df.loc[sentimental_df['target']==4,'target']=1

sentimental_df['target'].value_counts()

from datetime import datetime

def return_day_of_week(date):
    day_of_week = date.split(' ')[0]
    return day_of_week

def return_month(date):
    day_of_week = date.split(' ')[1]
    return day_of_week

def return_day(date):
    day_of_week = date.split(' ')[2]
    return day_of_week

def return_time(date):
    day_of_week = date.split(' ')[3]
    return day_of_week

def return_timezone(date):
    day_of_week = date.split(' ')[4]
    return day_of_week

def return_year(date):
    day_of_week = date.split(' ')[5]
    return day_of_week
    
sentimental_df['day_of_week']=sentimental_df['date'].apply(return_day_of_week)
sentimental_df['month']=sentimental_df['date'].apply(return_month)
sentimental_df['day']=sentimental_df['date'].apply(return_day)
sentimental_df['time']=sentimental_df['date'].apply(return_time)
sentimental_df['timezone']=sentimental_df['date'].apply(return_timezone)
sentimental_df['year']=sentimental_df['date'].apply(return_year)

sentimental_df['year'] = sentimental_df['year'].astype(int)
sentimental_df['day'] = sentimental_df['day'].astype(int)

sentimental_df.to_csv('sentimental_df.csv')

sentimental_df['text'][0]

sentimental_df['month'].value_counts()

sentimental_df['user'].value_counts()[:10000]

"""# New Section"""

len(set(sentimental_df['user']))

sentimental_df

"""## Distribution of sentiment"""

plt = sentimental_df.groupby('target')['target'].count().plot(kind='bar', title='Distribution of sentiment',color = ['#1f77b4', '#ff7f0e'],
                                               legend=False)
plt.set_xticklabels(['Negative','Positive'], rotation=0)
plt

"""As we can see from the graphs, we have equal number of Positive/Negative tweets. Both equaling to 800,000 tweets. This means our dataset is not skewed which makes working on the dataset easier for us.

##User Distribution
"""

sentimental_df['pos_ratio'] = sentimental_df.groupby('user')['target'].transform('sum')/sentimental_df.groupby('user')['target'].transform('count')
sentimental_df['total_post'] = sentimental_df.groupby('user')['user'].transform('size')

df=sentimental_df[['user', 'pos_ratio', 'total_post']].sort_values(by ='total_post', ascending=False)
pairs = list(zip(df['user'], df['pos_ratio']))
pairs = list(dict.fromkeys(pairs))
pairs = pairs[:10000]
arr = [i[1] for i in pairs]

import matplotlib.pyplot as plt
_=plt.hist(arr, rwidth=0.85)
plt.xlabel("proportion of positive emotion")
plt.ylabel("number of users")
plt.title("positive emotion proportion of top 10000 users")
plt.show()

"""### Emotion change over time"""

def return_pos_neg(month):
    pos, neg = [-1]*3, [-1]*3
    df = sentimental_df[(sentimental_df.month == month)]
    pos[0], pos[1], pos[2] = len(df[(df['day']<=10) & (df['target']==1)]), len(df[(df['day']>10) & (df['day']<=20) & (df['target']==1)]), len(df[(df['day']>20) & (df['target']==1)])
    neg[0], neg[1], neg[2] = len(df[(df['day']<=10) & (df['target']==0)]), len(df[(df['day']>10) & (df['day']<=20) & (df['target']==0)]), len(df[(df['day']>20) & (df['target']==0)])
    return pos, neg

pos, neg = [], []
for mon in sentimental_df['month'].unique():
    a, b = return_pos_neg(mon)
    pos.append(a)
    neg.append(b)

pos = [item for sublist in pos for item in sublist] 
neg = [item for sublist in neg for item in sublist] 

posBars = [i/(i+j) for i,j in zip(pos, neg)]
negBars = [j/(i+j) for i,j in zip(pos, neg)]

import matplotlib.pyplot as plt

def sumzip(*items):
    return [sum(values) for values in zip(*items)]

r = np.array(range(9))
fig, ax = plt.subplots()
ax.bar(r, posBars, color='#ff7f0e', edgecolor='white', width=0.85, label = 'pos emotion', align="center")
ax.bar(r, negBars, bottom=sumzip(posBars), color='#1f77b4', edgecolor='white', width=0.85, label = 'neg emotion', align="center")
plt.margins()

# Custom x axis
plt.xticks(r, ['Apr 1-10', 'Apr 11-20', 'Apr 21-30', 'May 1-10', 'May 11-20', 'May 21-31','Jun 1-10', 'Jun 11-20', 'Jun 21-30'],rotation=45)
plt.xlabel("date")
plt.title("emotion change over time")
plt.legend()
plt.show()

"""## Emotion text """

data_pos = list(sentimental_df[sentimental_df['target']==1]['text'])
data_neg =  list(sentimental_df[sentimental_df['target']==0]['text'])

# Import package
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt

# Generate word cloud
wc = WordCloud(width= 600, height = 600, random_state=1, background_color='salmon', colormap='Pastel1', collocations=False, stopwords = STOPWORDS).generate(" ".join(data_pos))
# Plot
plt.figure(figsize = (10,10))
plt.imshow(wc)

# Import package
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt

# Generate word cloud
wc = WordCloud(width= 600, height = 600, random_state=1, background_color='grey', colormap='Pastel1', collocations=False, stopwords = STOPWORDS).generate(" ".join(data_neg))
# Plot
plt.figure(figsize = (10,10))
plt.imshow(wc)

"""## CountVectorizer for EDA (Count top k words on full dataset)"""

import nltk
import re
import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader

import scipy as sp
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from scipy.sparse import coo_matrix,hstack

text = sentimental_df['text']

#get 100 most frequent words
vectorizer = CountVectorizer(max_features = 100)
words = vectorizer.fit_transform(text)

#sum the frequency of 100 most frequent words
sum_words = words.sum(axis=0)

#combine frequency with word
words_freq = [(word, sum_words[0, idx]) for word, idx in vectorizer.vocabulary_.items()]
words_freq =sorted(words_freq, key = lambda x: x[1], reverse=True)
print(words_freq)

words_df = pd.DataFrame(words_freq[:30], columns=['word', 'frequency'])
words_df.plot.scatter(x='word', y='frequency')

plt.xlabel('word', rotation=0)
plt.xticks(rotation =60)
plt.ylabel('frequency')
plt.title('Top 30 words frequency')
plt.show()

"""## Data Preprocessing (Replacing URL, Emoji, @username)

### Source idea: 
https://www.kaggle.com/stoicstatic/twitter-sentiment-analysis-for-beginners/notebook
"""

emojiPattern = {':)': 'smile', ':-)': 'smile', ';d': 'wink', ':-E': 'vampire', ':(': 'sad',  ':-(': 'sad', ':-<': 'sad', 
          ':P': 'raspberry', ':O': 'surprised', ':-@': 'shocked', ':@': 'shocked',':-$': 'confused', ':\\': 'annoyed', 
          ':#': 'mute', ':X': 'mute', ':^)': 'smile', ':-&': 'confused', '$_$': 'greedy', '@@': 'eyeroll', ';)': 'wink', 
          ':-!': 'confused', ':-D': 'smile', ':-0': 'yell', 'O.o': 'confused', '<(-_-)>': 'robot', 'd[-_-]b': 'dj', 
          ":'-)": 'sadsmile', ';-)': 'wink', 'O:-)': 'angel','O*-)': 'angel','(:-D': 'gossip', '=^.^=': 'cat'}

urlPattern = r"((http://)[^ ]*|(https://)[^ ]*|( www\.)[^ ]*)"
userPattern = '@[^\s]+'

new_text = []
for i in range(len(sentimental_df.text)):
    each_tweet = sentimental_df.text.iloc[i].lower()

    modified_tweet = re.sub(urlPattern,' URL', each_tweet)
    for emoji in emojiPattern.keys():
        modified_tweet = modified_tweet.replace(emoji, "EMOJI_" + emojiPattern[emoji])        
    modified_tweet = re.sub(userPattern,' USERNAME', modified_tweet)  
    new_text.append(modified_tweet)

sentimental_df['text'] = pd.Series(new_text)

sentimental_df.text

"""## Data Preprocessing (TfidfVectorizer)

"""

#data split
text = sentimental_df['text']
y = sentimental_df['target']
X_dev, X_test, y_dev, y_test = train_test_split(text,y, test_size=0.2, random_state=42)
X_train, X_val, y_train, y_val = train_test_split(X_dev, y_dev, test_size=0.25, random_state=42)

min_n = 1
max_n = 3
max_df = 0.8
k = None
tfidf_vec = TfidfVectorizer(ngram_range=(min_n,max_n),sublinear_tf=True,max_df=max_df,max_features = k)

tfidf_X_train = tfidf_vec.fit_transform(X_train)
tfidf_X_val = tfidf_vec.transform(X_val)
tfidf_X_test = tfidf_vec.transform(X_test)

## do not run 
import joblib
joblib.dump(tfidf_X_train, 'tfidf_X_train.pkl') 
joblib.dump(tfidf_X_val, 'tfidf_X_val.pkl') 
joblib.dump(tfidf_X_test, 'tfidf_X_test.pkl')

## we can load tfidf_X_train,val,test here directly
import joblib
tfidf_X_train = joblib.load('tfidf_X_train.pkl') 
tfidf_X_val = joblib.load('tfidf_X_val.pkl') 
tfidf_X_test = joblib.load('tfidf_X_test.pkl')

tfidf_X_train.shape

"""## Data Preprocessing (CountVectorizer)"""

min_n = 1
max_n = 3
max_df = 0.8
k = None
count_vec = CountVectorizer(ngram_range=(min_n,max_n),max_df=max_df,max_features = k)
count_X_train = tfidf_vec.fit_transform(X_train)
count_X_val = tfidf_vec.transform(X_val)
count_X_test = tfidf_vec.transform(X_test)

"""## Data Preprocessing Word2Vecv embedding"""

from gensim.models import Word2Vec

def train_word2vec(text,window_size, neg_sample,epochs=20):
    """
    This function train the word2vec embedding and save into a bin file
    """
    #remove punctuation
    tokenizer = nltk.RegexpTokenizer(r"\w+")
    word_list = [] 
    for sentence in text:
        token = tokenizer.tokenize(sentence.lower())
        word_list.append(token)
    #use the Word2Vec model to train embeddings
    model = Word2Vec(word_list, min_count=1,size= 100,workers=3, window =3)

    return model

word2vec_model = train_word2vec(text,2,25,epochs=15)

#save word2vec model
word2vec_model.save("word2vec.model")

model = Word2Vec.load("word2vec.model")

#don't need to run this
def get_tokens(df):
  df = df.reset_index(drop = True)
  tokens = []
  tokenizer = nltk.RegexpTokenizer(r"\w+")
  for i in range(len(df)):
    token = tokenizer.tokenize(df[i].lower())
    tokens.append(token)
  return tokens

#train_tokens = get_tokens(X_train)
#val_tokens = get_tokens(X_val)
#test_tokens = get_tokens(X_test)

#don't run this!
def get_sentence_embedding(model,data,dim = 100):
  emb_max = np.zeros((len(data),dim))
  emb_mean = np.zeros((len(data),dim))

  for i in range(len(data)):
    tokens = data[i]

    emb = np.zeros((len(tokens),dim))
    for j in range(len(tokens)):
      word = tokens[j]
      try:
        emb[j] = model.wv[word]
      except KeyError:
        emb = np.delete(emb,-1,0)

    emb_max[i] = np.amax(emb,axis = 0)
    emb_mean[i] = np.mean(emb,axis = 0)
  
  return emb_max,emb_mean

X_train_embmax, X_train_embmean = get_sentence_embedding(model,train_tokens)

X_val_embmax, X_val_embmean = get_sentence_embedding(model,val_tokens)

np.savetxt("X_train_embmax.csv", X_train_embmax , delimiter=",")

np.savetxt("X_train_embmean.csv", X_train_embmean , delimiter=",")

np.savetxt("X_val_embmax.csv", X_val_embmax , delimiter=",")
np.savetxt("X_val_embmean.csv", X_val_embmean , delimiter=",")

X_test_embmax, X_test_embmean = get_sentence_embedding(model,test_tokens)

np.savetxt("X_test_embmax.csv",X_test_embmax , delimiter=",")

np.savetxt("X_test_embmean.csv",X_test_embmean , delimiter=",")



X_train_embmean=pd.read_csv("X_train_embmean.csv",header=None)
X_train_embmax=pd.read_csv("X_train_embmax.csv",header=None)

X_val_embmean=pd.read_csv("X_val_embmean.csv",header=None)
X_val_embmax=pd.read_csv("X_val_embmax.csv",header=None)

X_test_embmean=pd.read_csv("X_test_embmean.csv",header=None)
X_test_embmax=pd.read_csv("X_test_embmax.csv",header=None)

"""## **Logistic Regression**

### Logistic Regression - tfidf
"""

from sklearn.linear_model import LogisticRegression

"""#### Hyperparameter tuning"""

# solvers = ['sag','newton-cg', 'lbfgs', 'liblinear']
# penalty =  ['l1', 'l2','elasticnet']
import datetime

l1_ratio = [0, 0.5, 1]
c_values = [0.01, 0.1]
val_scores = []
parameters = []
for l1 in l1_ratio:
  for c in c_values:
    clf = LogisticRegression(
                    C = c,
                    max_iter = 100,
                    tol = 0.0001,
                    solver = 'saga',
                    l1_ratio = l1,
                    fit_intercept = True,
                    penalty = 'elasticnet',
                    dual = False,
                    verbose = 0)
    start = datetime.datetime.now()
    clf.fit(tfidf_X_train, y_train)
    clf.predict(tfidf_X_val) 
    end = datetime.datetime.now()
    print(clf.score(tfidf_X_val, y_val), l1, c, (end-start).seconds)

    val_scores.append(clf.score(tfidf_X_val, y_val))
    parameters.append([l1,c])

max_item = max(val_scores)
index = val_scores.index(max_item)
optimal_parameters = parameters[index]
print("The optimal parameter for logistic regression is :", optimal_parameters)

"""#### Train"""

clf = LogisticRegression(
                    C = 0.1,
                    max_iter = 100,
                    tol = 0.0001,
                    solver = 'saga',
                    l1_ratio = 0,
                    fit_intercept = True,
                    penalty = 'elasticnet',
                    dual = False,
                    verbose = 0)
clf.fit(tfidf_X_train, y_train)

"""#### Predict"""

from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix

#Predict values based on new parameters

y_pred_acc = clf.predict(tfidf_X_test)

# New Model Evaluation metrics 
print('Accuracy Score: ' + str(accuracy_score(y_test, y_pred_acc)))
print('Precision Score: ' + str(precision_score(y_test, y_pred_acc)))
print('Recall Score: ' + str(recall_score(y_test, y_pred_acc)))
print('F1 Score: ' + str(f1_score(y_test, y_pred_acc)))

#Logistic Regression (Grid Search) Confusion matrix
confusion_matrix(y_test, y_pred_acc)

"""### Logistic Regression - embmean

#### Hyperparameter tuning
"""

# solvers = ['sag','newton-cg', 'lbfgs', 'liblinear']
# penalty =  ['l1', 'l2','elasticnet']
import datetime

l1_ratio = [0, 0.5, 1]
c_values = [0.01, 0.1]
val_scores = []
parameters = []
for l1 in l1_ratio:
  for c in c_values:
    clf = LogisticRegression(
                    C = c,
                    max_iter = 100,
                    tol = 0.0001,
                    solver = 'saga',
                    l1_ratio = l1,
                    fit_intercept = True,
                    penalty = 'elasticnet',
                    dual = False,
                    verbose = 0)
    start = datetime.datetime.now()
    clf.fit(X_train_embmean, y_train)
    clf.predict(X_val_embmean) 
    end = datetime.datetime.now()
    print(clf.score(X_val_embmean, y_val), l1, c, (end-start).seconds)

    val_scores.append(clf.score(X_val_embmean, y_val))
    parameters.append([l1,c])

"""#### Train"""

clf = LogisticRegression(
                    C = 0.01,
                    max_iter = 100,
                    tol = 0.0001,
                    solver = 'saga',
                    l1_ratio = 1,
                    fit_intercept = True,
                    penalty = 'elasticnet',
                    dual = False,
                    verbose = 0)
clf.fit(X_train_embmean, y_train)

"""#### Predict"""

#Predict values based on new parameters
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix

y_pred_acc = clf.predict(X_test_embmean)

# New Model Evaluation metrics 
print('Accuracy Score: ' + str(accuracy_score(y_test, y_pred_acc)))
print('Precision Score: ' + str(precision_score(y_test, y_pred_acc)))
print('Recall Score: ' + str(recall_score(y_test, y_pred_acc)))
print('F1 Score: ' + str(f1_score(y_test, y_pred_acc)))

#Logistic Regression (Grid Search) Confusion matrix
confusion_matrix(y_test, y_pred_acc)

"""## **SVM**

### SVM - tfidf

#### Hyperparameter tuning
"""

tfidf_X_train_svm = tfidf_X_train[0:10000]
tfidf_X_val_svm = tfidf_X_val[0:10000]
tfidf_X_test_svm = tfidf_X_test[0:10000]

from sklearn import svm

C = np.logspace(-1,1,10)
val_scores = []
parameters = []

for c in C:
    clf = svm.SVC(kernel='linear', C=c)
    clf.fit(tfidf_X_train_svm, y_train[0:10000])
    clf.predict(tfidf_X_val_svm) 
    print(clf.score(tfidf_X_val_svm, y_val[0:10000]))
    val_scores.append(clf.score(tfidf_X_val_svm, y_val[0:10000]))
    parameters.append(c)

print("Best test accuracy after hyperparameter tuning:", max(val_scores))

max_item = max(val_scores)
index = val_scores.index(max_item)
optimal_parameters = parameters[index]
print("The optimal parameter for logistic regression is :", optimal_parameters)

"""#### Train"""

clf = svm.SVC(kernel='linear', C=optimal_parameters)
clf.fit(tfidf_X_train_svm, y_train[0:10000])

"""#### Predict"""

from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix

#Predict values based on new parameters
y_pred_acc = clf.predict(tfidf_X_test_svm)

# New Model Evaluation metrics 
print('Accuracy Score : ' + str(accuracy_score(y_test[0:10000],y_pred_acc)))
print('Precision Score : ' + str(precision_score(y_test[0:10000],y_pred_acc)))
print('Recall Score : ' + str(recall_score(y_test[0:10000],y_pred_acc)))
print('F1 Score : ' + str(f1_score(y_test[0:10000],y_pred_acc)))

#Logistic Regression (Grid Search) Confusion matrix
confusion_matrix(y_test[0:10000],y_pred_acc)

"""### SVM - embmean

#### Hyperparameter tuning
"""

X_train_embmean_svm = X_train_embmean[0:10000]
X_val_embmean_svm = X_val_embmean[0:10000]
X_test_embmean_svm = X_test_embmean[0:10000]
y_train_svm = y_train[0:10000]
y_val_svm = y_val[0:10000]
y_test_svm = y_test[0:10000]

from sklearn import svm
C = np.logspace(-1,1,10)
val_scores = []
parameters = []

for c in C:
    clf = svm.SVC(kernel='linear', C=c)
    clf.fit(X_train_embmean_svm, y_train_svm)
    clf.predict(X_val_embmean_svm) 
    score=clf.score(X_val_embmean_svm, y_val_svm)
    print(c, score)
    val_scores.append(score)
    parameters.append(c)

print("Best test accuracy after hyperparameter tuning:", max(val_scores))

max_item = max(val_scores)
index = val_scores.index(max_item)
optimal_parameters = parameters[index]
print("The optimal parameter for logistic regression is :", optimal_parameters)

"""#### Training"""

clf = svm.SVC(kernel='linear', C=optimal_parameters)
clf.fit(X_train_embmean_svm, y_train_svm)

"""#### Predict"""

from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix

#Predict values based on new parameters
y_pred_acc = clf.predict(X_test_embmean_svm)

# New Model Evaluation metrics 
print('Accuracy Score : ' + str(accuracy_score(y_test_svm,y_pred_acc)))
print('Precision Score : ' + str(precision_score(y_test_svm,y_pred_acc)))
print('Recall Score : ' + str(recall_score(y_test_svm,y_pred_acc)))
print('F1 Score : ' + str(f1_score(y_test_svm,y_pred_acc)))

#Logistic Regression (Grid Search) Confusion matrix
confusion_matrix(y_test_svm,y_pred_acc)

"""## **KNN**

### KNN - tfidf

#### Hyperparameter tuning
"""

tfidf_X_train

tfidf_X_train_knn = tfidf_X_train[0:10000]
tfidf_X_val_knn = tfidf_X_val[0:10000]
tfidf_X_test_knn = tfidf_X_test[0:10000]
y_train_knn = y_train[0:10000]
y_val_knn = y_val[0:10000]
y_test_knn = y_test[0:10000]

from sklearn.neighbors import KNeighborsClassifier

val_scores = []
neighbors = np.arange(1,40,2)
for idx in neighbors:
    knn = KNeighborsClassifier(n_neighbors = idx)
    knn.fit(tfidf_X_train_knn,y_train_knn)
    score = knn.score(tfidf_X_val_knn, y_val_knn)
    print(score)
    val_scores.append(score)

print(f"Best validation score:, {np.max(val_scores):.3f}")
best_n_neighbors = neighbors[np.argmax(val_scores)]
print("Best # of neighbors:" , best_n_neighbors)

"""#### Train"""

knn = KNeighborsClassifier(n_neighbors = best_n_neighbors)
knn.fit(tfidf_X_train_knn,y_train_knn)
y_pred_acc = clf.predict(tfidf_X_test_knn)

"""#### Predict"""

# New Model Evaluation metrics 
print('Accuracy Score : ' + str(accuracy_score(y_test_knn,y_pred_acc)))
print('Precision Score : ' + str(precision_score(y_test_knn,y_pred_acc)))
print('Recall Score : ' + str(recall_score(y_test_knn,y_pred_acc)))
print('F1 Score : ' + str(f1_score(y_test_knn,y_pred_acc)))

#Logistic Regression (Grid Search) Confusion matrix
confusion_matrix(y_test_knn,y_pred_acc)

"""### KNN - embmean

#### Hyperparameter tuning
"""

X_train_embmean_knn = X_train_embmean[0:10000]
X_val_embmean_knn = X_val_embmean[0:10000]
X_test_embmean_knn = X_test_embmean[0:10000]
y_train_knn = y_train[0:10000]
y_val_knn = y_val[0:10000]
y_test_knn = y_test[0:10000]

"""#### Train"""

from sklearn.neighbors import KNeighborsClassifier
val_scores = []
neighbors = np.arange(1,20,2)
for idx in neighbors:
    knn = KNeighborsClassifier(n_neighbors = idx)
    knn.fit(X_train_embmean_knn,y_train_knn)
    val_scores.append(knn.score(X_val_embmean_knn,y_val_knn))
print(f"Best validation score:, {np.max(val_scores):.3f}")
best_n_neighbors = neighbors[np.argmax(val_scores)]
print("Best # of neighbors:" , best_n_neighbors)

from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix

knn = KNeighborsClassifier(n_neighbors = best_n_neighbors)
knn.fit(X_train_embmean_knn,y_train_knn)
y_pred_acc = knn.predict(X_test_embmean_knn)

# New Model Evaluation metrics 
print('Accuracy Score : ' + str(accuracy_score(y_test_knn,y_pred_acc)))
print('Precision Score : ' + str(precision_score(y_test_knn,y_pred_acc)))
print('Recall Score : ' + str(recall_score(y_test_knn,y_pred_acc)))
print('F1 Score : ' + str(f1_score(y_test_knn,y_pred_acc)))

#Logistic Regression (Grid Search) Confusion matrix
confusion_matrix(y_test_knn,y_pred_acc)

"""## Decision Tree"""

from sklearn.tree import DecisionTreeClassifier
from sklearn.compose import make_column_transformer
from sklearn.model_selection import GridSearchCV
from sklearn.calibration import CalibratedClassifierCV, CalibrationDisplay

"""### Decision Tree - tfidf"""

tfidf_X_train_dtc = tfidf_X_train[0:10000]
tfidf_X_val_dtc = tfidf_X_val[0:10000]
tfidf_X_test_dtc = tfidf_X_test[0:10000]
y_train_dtc = y_train[0:10000]
y_val_dtc = y_val[0:10000]
y_test_dtc = y_test[0:10000]

"""#### hyperparameter tuning"""

max_depths = [100,150,200,250,300]
val_scores = []

for each in max_depths:
    dtc = DecisionTreeClassifier(max_depth = each)
    dtc.fit(tfidf_X_train_dtc,y_train_dtc)
    score = dtc.score(tfidf_X_val_dtc, y_val_dtc)
    print(score)
    val_scores.append(score)

print(f"Best validation score:, {np.max(val_scores):.3f}")
best_depth = max_depths[np.argmax(val_scores)]
print("Best # of neighbors:" , best_depth)

"""#### train"""

dtc_model = DecisionTreeClassifier(random_state=42, max_depth=best_depth)
dtc_model.fit(tfidf_X_train_dtc, y_train_dtc)

"""#### evaluate"""



#Predict values based on new parameters
y_pred_acc = dtc_model.predict(tfidf_X_test_dtc)

# New Model Evaluation metrics 
print('Accuracy Score : ' + str(accuracy_score(y_test_dtc,y_pred_acc)))
print('Precision Score : ' + str(precision_score(y_test_dtc,y_pred_acc)))
print('Recall Score : ' + str(recall_score(y_test_dtc,y_pred_acc)))
print('F1 Score : ' + str(f1_score(y_test_dtc,y_pred_acc)))

#Logistic Regression (Grid Search) Confusion matrix
confusion_matrix(y_test_dtc,y_pred_acc)

"""## XGB"""

!pip install xgboost --upgrade

from xgboost import XGBClassifier

"""### XGB - tfidf"""

tfidf_X_train_xgb = tfidf_X_train[0:10000]
tfidf_X_val_xgb = tfidf_X_val[0:10000]
tfidf_X_test_xgb = tfidf_X_test[0:10000]
y_train_xgb = y_train[0:10000]
y_val_xgb = y_val[0:10000]
y_test_xgb = y_test[0:10000]

"""#### hyperparameter tuning"""

lrates = [0.05,0.1,0.2,0.3]
val_scores = []

for each in lrates:
    xgb = XGBClassifier(use_label_encoder=False, eval_metric='logloss', learning_rate=each, random_state=42)
    xgb.fit(tfidf_X_train_xgb,y_train_xgb)
    score = xgb.score(tfidf_X_val_xgb, y_val_xgb)
    print(score)
    val_scores.append(score)

print(f"Best validation score:, {np.max(val_scores):.3f}")
best_lrate = lrates[np.argmax(val_scores)]
print("Best # of neighbors:" , best_lrate)

"""#### train"""

xgb_model = XGBClassifier(use_label_encoder=False, eval_metric='logloss', learning_rate=best_lrate, random_state=42)
xgb_model.fit(tfidf_X_train_xgb, y_train_xgb)

"""#### evaluate"""

#Predict values based on new parameters
y_pred_acc = xgb_model.predict(tfidf_X_test_xgb)

# New Model Evaluation metrics 
print('Accuracy Score : ' + str(accuracy_score(y_test_xgb,y_pred_acc)))
print('Precision Score : ' + str(precision_score(y_test_xgb,y_pred_acc)))
print('Recall Score : ' + str(recall_score(y_test_xgb,y_pred_acc)))
print('F1 Score : ' + str(f1_score(y_test_xgb,y_pred_acc)))

#Logistic Regression (Grid Search) Confusion matrix
confusion_matrix(y_test_xgb,y_pred_acc)

