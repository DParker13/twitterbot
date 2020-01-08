import tweepy, time, sys, datetime
import os as environ

class BotInfo:

    def __init__(self):
        #bot settings to look more human
        self.USERNAME = "NormanRoss04"
        self.FOLLOWER_LIMIT = 1901
        self.TWEET_SEARCH_LIMIT = 25
        self.SEARCH_TIMER = 17 * 60
        self.LIKE_RETWEET_ONLY_TIMER = 15 * 60
        self.TWEET_LIMIT_PER_SEARCH = 5
        self.RUNS_BEFORE_SWITCH = 4
        self.OVERFLOW_SEARCH_REPEAT = 3
        self.OVERFLOW_EXTRA_SEARCHES = 20
        self.total_tweets_since_start = 0

    def setSettings(self, username, follower_limit, tweet_search_limit, search_timer, like_retweet_only_timer, tweet_limit_per_search, runs_before_switch, overflow_search_repeat, overflow_extra_searches):
        #bot settings to look more human
        self.USERNAME = username
        self.FOLLOWER_LIMIT = int(follower_limit)
        self.TWEET_SEARCH_LIMIT = int(tweet_search_limit)
        self.SEARCH_TIMER = int(search_timer) * 60
        self.LIKE_RETWEET_ONLY_TIMER = int(like_retweet_only_timer) * 60
        self.TWEET_LIMIT_PER_SEARCH = int(tweet_limit_per_search)
        self.RUNS_BEFORE_SWITCH = int(runs_before_switch)
        self.OVERFLOW_SEARCH_REPEAT = int(overflow_search_repeat)
        self.OVERFLOW_EXTRA_SEARCHES = int(overflow_extra_searches)
        self.total_tweets_since_start = 0

    def stopBot():
        run_loop = False

    consumer_key = environ['CONSUMER_KEY']
    consumer_secret = environ['CONSUMER_SECRET']
    access_token = environ['ACCESS_KEY']
    access_token_secret = environ['ACCESS_SECRET']

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)

    #number of days to go back in time for the search date
    goBackTime = 0
    date_since = (datetime.datetime.now() - datetime.timedelta(days=goBackTime)).date()
    print(date_since)

    #defines search terms
    search_words = ["retweet to win", "retweet giveaway", "crypto retweet giveaway", "steam giveaway retweet"]
    filtered_words = ["bot", "b0t", "tag", "comment", "screenshot", "proof", "sugardaddy", "sugarbaby", "robux"]
    filtered_users = ["bot", "b0t", "muckzuckerburg", "retweeejt"]

    #emergency stop
    run_loop = True
