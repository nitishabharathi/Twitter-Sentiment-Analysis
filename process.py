import pandas as pd
import matplotlib.pyplot as plt
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import numpy as np
import json
import re

tweets_data_path = 'indvsnz.csv'
tweets_data = []
tweets_file = open(tweets_data_path, "r")
for line in tweets_file:
    try:
        tweet = json.loads(line)
        tweets_data.append(tweet)
    except:
        continue

stopWords = []

stopWords.append('AT_USER')
stopWords.append('url')
stopWords.append('rt')

def processTweet(tweet):
    # process the tweets
    featureVector = []
    #Convert to lower case
    tweet=tweet.lower()
    #tweet = tweet.lower()
    tweet = re.sub(r'\$\w*','',tweet) # Remove tickers
    #Convert www.* or https?://* to URL
    tweet = re.sub('((www\.[^\s]+)|(https?://[^\s]+))','',tweet)
    #Convert @username to AT_USER
    tweet = re.sub('@[^\s]+','',tweet)
    #tweet = re.sub(r'['+string.punctuation+']+', ' ',tweet) # Remove puncutations like 's
    tweet=re.sub(r'[^\x00-\x7F]+',' ',tweet)
    tweet = re.sub('[\s]+', ' ', tweet)
    #Replace #word with word
    tweet = re.sub(r'#([^\s]+)', r'\1', tweet)
    #trim
    tweet = tweet.strip('\'"')
    wordss = tweet.split()
 
    for w in wordss:
              
              if(w in stopWords):
                  continue
              else:
                  featureVector.append(w)
   
    return tweet

tweets = pd.DataFrame()
index = 0
for num, line in enumerate(tweets_data):
  try:
      tweets.loc[index,'text'] = line['text']
      tweets.loc[index,'lang']=line['lang']
      tweets.loc[index,'processedTweet']=processTweet(line['text'])
      tweets.loc[index,'created']=line['created_at']
      index = index + 1 
      print(num)
  except:
      print (num, "line not parsed")
      continue
tweets['processedTweet'].replace('', np.nan, inplace=True) 
tweets.dropna(subset=['processedTweet'], inplace=True)
tweets.to_csv('maindb.csv')

