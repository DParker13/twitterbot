import tweepy, time, sys, datetime

class BotInfo:

    #bot settings to look more human
    def __init__(self):
        #account info
        self.USERNAME = "NormanRoss04"
        self.CASHAPP = "NormanRoss04"

        #search settings
        self.TWEET_SEARCH_LIMIT = 25
        self.SEARCH_TIMER = 17 * 60
        self.LIKE_RETWEET_ONLY_TIMER = 15 * 60
        self.TWEET_LIMIT_PER_SEARCH = 5
        self.RUNS_BEFORE_SWITCH = 4
        self.OVERFLOW_SEARCH_REPEAT = 3
        self.OVERFLOW_EXTRA_SEARCHES = 20

        #limits before removing old tweets or likes
        self.TWEET_LIMIT = 3000
        self.TWEET_RESET_LIMIT = 1000
        self.FRIEND_LIMIT = 1901
        self.FRIEND_RESET_LIMIT = 1400

        #dates
        self.GO_BACK_TIME = 5
        self.DELETE_DATE = datetime.datetime.utcnow() - datetime.timedelta(days=self.GO_BACK_TIME)

        #counters
        self.total_tweets_since_start = 0

    consumer_key = 'jgKcJ535zMUd8H8yYibroFgFi'
    consumer_secret = 'TxgRXsBVsPy2R6J26eMMqpuV8kM3GCHS3TM9ZRnLrlCT4z9f7W'
    access_token = '1711405795-DyzMGIBehxXsCBnaipaCvdOtGMX79FWvq4yntx6'
    access_token_secret = '07vqgbGf7oXfqLdKnjgbrLE06yWj7cIYAJdFW6MSXevrr'

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
    filtered_words = ["bot", "b0t", "comment", "screenshot", "proof", "sugar", "sugardaddy", "sugarbaby", "robux", "sugar baby", "sugar momma", "porn", "roblox", "sex", "fortnite"]
    filtered_users = ["bot", "b0t", "spotter", "sp0tter", "followandrt2win", "muckzuckerburg", "retweeejt"]
