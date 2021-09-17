import tweepy, time, sys, datetime
from os import environ


class BotInfo:

    # bot settings to look more human
    def __init__(self):
        # account info
        self.USERNAME = "NormanRoss04"
        self.CASHAPP = "NormanRoss04"

        # search settings
        self.TWEET_SEARCH_LIMIT = 25
        self.SEARCH_TIMER = 30 * 60
        self.LIKE_RETWEET_ONLY_TIMER = 30 * 60
        self.TWEET_LIMIT_PER_SEARCH = 5
        self.RUNS_BEFORE_SWITCH = 4
        self.OVERFLOW_SEARCH_REPEAT = 3
        self.OVERFLOW_EXTRA_SEARCHES = 20

        # limits before removing old tweets or likes
        self.TWEET_LIMIT = 3000
        self.TWEET_RESET_LIMIT = 1000
        self.FRIEND_LIMIT = 2600
        self.FRIEND_RESET_LIMIT = 1200

        # dates
        self.GO_BACK_TIME = 5
        self.DELETE_DATE = datetime.datetime.utcnow() - datetime.timedelta(days=self.GO_BACK_TIME)

        # counters
        self.total_tweets_since_start = 0

    api_key = environ['API_KEY']
    api_secret = environ['API_SECRET']
    access_token = environ['ACCESS_TOKEN']
    access_token_secret = environ['ACCESS_SECRET']
    bearer_token = environ['BEARER_TOKEN']
    USERNAME = environ['USERNAME']
    CASHAPP = environ['CASHAPP']

    auth = tweepy.OAuthHandler(api_key, api_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

    # number of days to go back in time for the search date
    goBackTime = 0
    date_since = (datetime.datetime.now() - datetime.timedelta(days=goBackTime)).date()
    print(date_since)

    # defines search terms
    tag_list = ["James64705453", "CHRISTYSWEENEY1", "WippydeeWaen", "peppers_jay", "Crayola888", "Goog1234Hey",
                "Molex2_5"]
    search_words_main = ["retweet to win", "retweet giveaway", "steam giveaway", "game giveaway", "giftcard giveaway"]
    search_words_backup = ["like to win", "giveaway", "steam giveaway", "game giveaway", "giftcard giveaway"]
    filtered_words = ["bot", "b0t", "comment", "screenshot", "proof", "sugar", "sugardaddy", "sugarbaby", "robux",
                      "sugar baby", "sugar momma", "porn", "roblox", "sex", "fortnite", "vbuck", "account"]
    filtered_users = ["bot", "b0t", "spotter", "sp0tter", "sugar", "sugardaddy", "sugarbaby", "robux", "sugar baby",
                      "sugar momma", "porn", "roblox", "sex", "fortnite", "vbuck", "followandrt2win", "muckzuckerburg",
                      "retweeejt", "SookRiviegrave1", "munching1983", "Mary1983sel", "FaBell85_Ind"]
