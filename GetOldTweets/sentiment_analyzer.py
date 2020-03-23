import got3 as got
import numpy as np
import re
import requests
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import time

class SentimentAnalyzer():
    #Fetch a number of tweets for a certain keyword for a certain date span.
    #keyword is a query like "elizabeth warren"
    #max_tweets is the max number of tweets to fetch
    def _fetch_tweets(self, keyword, start_date, end_date, max_tweets=10):
        print("START", start_date)
        #Set the criteria
        tweetCriteria = got.manager.TweetCriteria().setQuerySearch(keyword).\
        setSince(start_date).setUntil(end_date).setMaxTweets(max_tweets)

        #Fetch the tweets
        tweets = got.manager.TweetManager.getTweets(tweetCriteria)

        #Make it a list
        tweet_list=[]
        for tweet in tweets:
            tweet_list.append(tweet.text)

        time.sleep(2)

        return tweet_list

    #Helper function to remove a given pattern from txt
    def _remove_pattern(self, input_txt, pattern):
        r = re.findall(pattern, input_txt)
        for i in r:
            input_txt = re.sub(i, '', input_txt)
        return input_txt

    #Cleans all tweets in the tweet list
    def _clean_tweets(self, lst):
        # remove twitter Return handles (RT @xxx:)
        lst = np.vectorize(self._remove_pattern)(lst, "RT @[\w]*:")
        # remove twitter handles (@xxx)
        lst = np.vectorize(self._remove_pattern)(lst, "@[\w]*")
        # remove URL links (httpxxx)
        lst = np.vectorize(self._remove_pattern)(lst, "https?://[A-Za-z0-9./]*")
        # remove special characters, numbers, punctuations (except for #)
        lst = np.core.defchararray.replace(lst, "[^a-zA-Z#]", " ")

        return lst

    #Gets the average sentiment of a tweet list
    def _get_average_sentiment(self, tweet_list):
        analyser = SentimentIntensityAnalyzer()

        scores = []
        for tweet in tweet_list:
            scores.append(analyser.polarity_scores(tweet)['compound'])

        return sum(scores)/len(scores)

    #Sentiment score for a given keyword on a given day.
    def get_sentiment_for_keyword(self, keyword, start_date, end_date):
        tweet_list = self._fetch_tweets(keyword, start_date, end_date)
        if not tweet_list:
            time.sleep(1)
            return 0.0
        tweet_list_clean = self._clean_tweets(tweet_list)
        return self._get_average_sentiment(tweet_list_clean)
