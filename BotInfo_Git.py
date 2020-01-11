import tweepy, time, sys, datetime
from os import environ

class BotInfo:

    def __init__(self):
        #bot settings to look more human
        #self.USERNAME = "NormanRoss04" ---Depricated
        #self.CASHAPP = "NormanRoss04" ---Depricated
        self.FOLLOWER_LIMIT = 1901
        self.TWEET_SEARCH_LIMIT = 25
        self.SEARCH_TIMER = 17 * 60
        self.LIKE_RETWEET_ONLY_TIMER = 15 * 60
        self.TWEET_LIMIT_PER_SEARCH = 5
        self.RUNS_BEFORE_SWITCH = 4
        self.OVERFLOW_SEARCH_REPEAT = 3
        self.OVERFLOW_EXTRA_SEARCHES = 20
        self.total_tweets_since_start = 0

    consumer_key = environ['CONSUMER_KEY']
    consumer_secret = environ['CONSUMER_SECRET']
    access_token = environ['ACCESS_KEY']
    access_token_secret = environ['ACCESS_SECRET']
    USERNAME = environ['USERNAME']
    CASHAPP = environ['CASHAPP']

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)

    #number of days to go back in time for the search date
    goBackTime = 0
    date_since = (datetime.datetime.now() - datetime.timedelta(days=goBackTime)).date()
    print(date_since)

    #defines search terms
    search_words = ["retweet to win", "retweet giveaway", "cashapp retweet giveaway", "steam giveaway retweet"]
    filtered_words = ["bot", "b0t", "tag", "comment", "screenshot", "proof", "sugardaddy", "sugarbaby", "robux"]
    filtered_users = ["bot", "b0t", "muckzuckerburg", "retweeejt"]

    #emergency stop
    run_loop = True
