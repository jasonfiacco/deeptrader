import got3 as got

tweetCriteria = got.manager.TweetCriteria().setQuerySearch("elizabeth warren").setSince("2018-01-11").setUntil("2018-02-12").setMaxTweets(10)
tweets = got.manager.TweetManager.getTweets(tweetCriteria)

for tweet in tweets:
    print(tweet.text)
