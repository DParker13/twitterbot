import tweepy, time, sys, datetime
from os import environ

class BotInfo:

    def __init__(self):
        #bot settings to look more human
        self.FRIEND_LIMIT = 1901
        self.FRIEND_RESET_LIMIT = 1400
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
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

    #number of days to go back in time for the search date
    goBackTime = 0
    date_since = (datetime.datetime.now() - datetime.timedelta(days=goBackTime)).date()
    print(date_since)

    #defines search terms
    tag_list = ["tradesecretbiz", "BeatlemaniaUK", "SJB6991"]
    search_words = ["retweet to win", "retweet giveaway", "cashapp retweet giveaway", "steam giveaway retweet"]
    filtered_words = ["bot", "b0t", "tag", "comment", "screenshot", "proof", "sugar", "sugardaddy", "sugarbaby", "robux", "sugar baby", "sugar momma", "porn", "roblox"]
    filtered_users = ["bot", "b0t", "spotter", "sp0tter", "followandrt2win", "muckzuckerburg", "retweeejt"]
