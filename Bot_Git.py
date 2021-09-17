import datetime
import random
import time
import tweepy
import traceback
import sys


class Bot:
    def RunMainBot(self, bot_info):
        print("\nRUNNING MAIN BOT-----------------", datetime.datetime.now().strftime("%H:%M:%S"))
        while True:
            display_counter = 1
            new_tweet_counter = 0

            # runs through all custom searches and finds tweets within this search
            for current_search in bot_info.search_words_main:
                # adds filters to the main search word to remove retweets and replies
                filtered_search = current_search + " -filter:retweets -filter:replies"

                # initializes counters to 0 for extra info after the search
                current_search_counter = 0
                already_retweeted_counter = 0

                print("\n--Search #", display_counter, "-- ", current_search, " --",
                      datetime.datetime.now().strftime("%H:%M:%S"))

                # tries different search sizes until tweet limit is reached or all tweets fail
                while current_search_counter < bot_info.TWEET_LIMIT_PER_SEARCH:
                    time.sleep(5)

                    # grabs all the tweets and decides whether or not to like, retweet, or follow them
                    for tweet in tweepy.Cursor(bot_info.api.search, q=filtered_search, lang="en",
                                               since=bot_info.date_since, tweet_mode="extended",
                                               result_type="mixed").items(bot_info.TWEET_SEARCH_LIMIT):
                        if current_search_counter > bot_info.TWEET_LIMIT_PER_SEARCH and bot_info.TWEET_LIMITER:
                            print("Tweet limit reached for search")
                            break

                        # gathers tweet information for debugging or allowing for more information
                        user = tweet.user
                        tweet_id = tweet.id
                        url = 'https://twitter.com/' + user.screen_name + '/status/' + str(tweet_id)

                        # some tweets are longer than normal and require different ways to gather the tweet text
                        try:
                            text = tweet.retweeted_status.full_text.lower()
                        except:
                            text = tweet.full_text.lower()

                        # checks the tweet for any competition rules that can't work with this bot
                        tweet_passes_filter = True
                        for word_filter in bot_info.filtered_words:
                            if word_filter in text:
                                print("\tFailed filter because of word: \"" + word_filter + "\" - " + url)
                                tweet_passes_filter = False
                                break

                        # skips the rest of the filters if it fails the tests
                        if not tweet_passes_filter:
                            continue

                        # check for bot spotters or other annoying users
                        for user_filter in bot_info.filtered_users:
                            if user_filter in user.screen_name.lower() or user_filter in user.name.lower():
                                print("\tBot Spotter avoided: " + user.screen_name + " - " + url)
                                tweet_passes_filter = False
                                break

                        # only likes, retweets, or follows if the tweet passes all the filters
                        if tweet_passes_filter:
                            retweet_status = Bot.retweet(url, bot_info, tweet, text)

                            if retweet_status != 0:
                                print("\tSuccessfully passed filters - " + url)
                                self.follow(bot_info, tweet, text, user)
                                Bot.tag(bot_info, text, user, tweet_id)
                                Bot.cash_app(bot_info, text, user, tweet_id)
                                Bot.like(tweet, text)
                                current_search_counter += 1
                                new_tweet_counter += 1
                            else:
                                already_retweeted_counter += 1

                    if current_search_counter == 0:
                        print("\tAll tweets failed filter!")
                    else:
                        print("\tAlready Retweeted: ", already_retweeted_counter)
                        print("\tCurrent Search - New Tweets: ", current_search_counter)
                    if current_search_counter is None:
                        print("ERROR: TWEET COUNTER = NONE")

                display_counter += 1

            print("\nCurrent Run Finished----")
            print("Time: ", datetime.datetime.now().strftime("%H:%M:%S"))
            print("New Tweets: ", new_tweet_counter)
            print("Total Tweets: ", bot_info.total_tweets_since_start)
            time.sleep(bot_info.SEARCH_TIMER * 60)

    # This is a backup version of the bot that does not follow users when the follow limit is reached
    def BackupBot(self, bot_info):
        print("\nRUNNING IN LIKE AND RETWEET ONLY MODE--------------", datetime.datetime.now().strftime("%H:%M:%S"))
        custom_filtered_words = bot_info.filtered_words + ["follow"]
        switch_counter = 0

        time.sleep(10)
        while True:
            display_counter = 1
            new_tweet_counter = 0

            # checks if backupbot has run long enough to attempt running mainbot again
            if switch_counter >= bot_info.RUNS_BEFORE_SWITCH:
                self.RunMainBot(bot_info)

            # runs through all custom searches and finds tweets within this search
            for current_search in bot_info.search_words_backup:
                # adds filters to the main search word to remove retweets and replies
                filtered_search = current_search + " -filter:retweets -filter:replies"

                # initializes counters to 0 for extra info after the search
                current_search_counter = 0
                already_retweeted_counter = 0

                print("\n--Search #", display_counter, "-- ", current_search, " --",
                      datetime.datetime.now().strftime("%H:%M:%S"))

                # tries different search sizes until tweet limit is reached or all tweets fail
                while current_search_counter < bot_info.TWEET_LIMIT_PER_SEARCH:
                    time.sleep(5)

                    # grabs all the tweets and decides whether or not to like or retweet (following has been removed)
                    for tweet in tweepy.Cursor(bot_info.api.search, q=filtered_search, lang="en",
                                               since=bot_info.date_since, tweet_mode="extended",
                                               result_type="mixed").items(bot_info.TWEET_SEARCH_LIMIT):
                        if current_search_counter > bot_info.TWEET_LIMIT_PER_SEARCH and bot_info.TWEET_LIMITER:
                            print("Tweet limit reached for search")
                            break

                        # gathers tweet information for debugging or allowing for more information
                        user = tweet.user
                        tweet_id = tweet.id
                        url = 'https://twitter.com/' + user.screen_name + '/status/' + str(tweet_id)

                        # some tweets are longer than normal and require different ways to gather the tweet text
                        try:
                            text = tweet.retweeted_status.full_text.lower()
                        except:
                            text = tweet.full_text.lower()

                        # checks the tweet for any competition rules that can't work with this bot
                        tweet_passes_filter = True

                        for word_filter in custom_filtered_words:
                            if word_filter in text:
                                print("\tFailed filter because of word: \"" + word_filter + "\" - " + url)
                                tweet_passes_filter = False
                                break

                        # skips the rest of the filters if it fails the tests
                        if not tweet_passes_filter:
                            continue

                        # check for bot spotters or other annoying users
                        for user_filter in bot_info.filtered_users:
                            if user_filter in user.screen_name.lower() or user_filter in user.name.lower():
                                print("\tBot Spotter avoided: " + user.screen_name + " - " + url)
                                tweet_passes_filter = False
                                break

                        # likes, retweets, or adds cashapp username if the tweet passes all the filters
                        if tweet_passes_filter:
                            retweet_status = Bot.retweet(url, bot_info, tweet, text)

                            if retweet_status != 0:
                                print("\tSuccessfully passed filters - " + url)

                                self.tag(bot_info, text, user, tweet_id)
                                Bot.cash_app(bot_info, text, user, tweet_id)
                                Bot.like(tweet, text)

                                current_search_counter += 1
                                new_tweet_counter += 1
                            else:
                                already_retweeted_counter += 1

                    if current_search_counter == 0:
                        print("\tAll tweets failed filter!")
                    else:
                        print("\tAlready Retweeted: ", already_retweeted_counter)
                        print("\tCurrent Search - New Tweets: ", current_search_counter)
                    if current_search_counter is None:
                        print("ERROR: TWEET COUNTER = NONE")

                display_counter += 1

            switch_counter += 1
            print("\nCurrent Run Finished----")
            print("Time: ", datetime.datetime.now().strftime("%H:%M:%S"))
            print("New Tweets: ", new_tweet_counter)
            print("Total Tweets: ", bot_info.total_tweets_since_start)
            time.sleep(bot_info.LIKE_RETWEET_ONLY_TIMER * 60)

    # TEST CODE
    def TestCodeOne(self, bot_info):
        test_search = "retweet tag" + " -filter:retweets -filter:replies"

        for tweet in tweepy.Cursor(bot_info.api.search, q=test_search, lang="en", since=bot_info.date_since,
                                   tweet_mode="extended").items(1):
            user = tweet.user
            tweet_id = tweet.id
            url = 'https://twitter.com/' + user.screen_name + '/status/' + str(tweet_id)

            try:
                text = tweet.retweeted_status.full_text.lower()
            except:
                text = tweet.full_text.lower()

            self.tag(bot_info, text, user, tweet_id)
            print("User - screen_name: " + user.screen_name)
            print("URL: " + url)

    def follow(self, bot_info, tweet, text, user):
        if "follow" in text:
            try:
                to_follow = [user.screen_name] + [i['screen_name'] for i in tweet.entities['user_mentions']]

                for screen_name in list(set(to_follow)):
                    bot_info.api.create_friendship(screen_name)
                    print('\t' + "Followed: " + screen_name)

            except tweepy.TweepError as e:
                if "161" in e.response.text:
                    print("Follow limit reached!")
                    self.BackupBot(bot_info)
                elif "261" in e.response.text:
                    print("Follow error! Most likely API is restricted to read only")
                    self.BackupBot(bot_info)
                else:
                    print(e)
                    print("ERROR Following")

    @staticmethod
    def like(tweet, text):
        if "like" in text or "fav" in text:
            try:
                tweet.favorite()
                print('\tLiked')
            except tweepy.TweepError as e:
                pass  # Do nothing

    @staticmethod
    def retweet(url, bot_info, tweet, text):
        if "retweet" in text or "rt" in text:
            if not tweet.retweeted:
                try:
                    tweet.retweet()
                    print("\tRetweeted")
                    bot_info.total_tweets_since_start += 1
                    return 1
                except tweepy.TweepError as e:
                    if "261" in e.response.text:
                        print("Follow error! Most likely API is restricted to read only")
                        traceback.print_exc()
                        sys.exit(3)
                    else:
                        print("\t\tError retweeting: " + e.response.text)
                    return 0
            else:
                print("\tAlready retweeted - " + url)
                return 0

        print("\tNo retweet in text - " + url)
        return 0

    @staticmethod
    def tag(bot_info, text, user, tweet_id):
        if "tag" in text:
            people_to_tag = []
            followers_list = random.sample(bot_info.tag_list, 3)

            tag_index = text.index("tag")

            if text.find("2", tag_index) != -1 or text.find("two", tag_index) != -1:
                people_to_tag.append(followers_list[0])
                people_to_tag.append(followers_list[1])
            elif text.find("3", tag_index) != -1 or text.find("three", tag_index) != -1:
                people_to_tag.append(followers_list[0])
                people_to_tag.append(followers_list[1])
                people_to_tag.append(followers_list[2])
            else:
                people_to_tag.append(followers_list[0])

            Bot.tag_people(bot_info, text, user, people_to_tag, tweet_id)

    @staticmethod
    def tag_people(bot_info, text, user, people_to_tag, tweet_id):
        # adds user to the reply
        reply = "@" + user.screen_name + "\n"

        # appends my "friends" usernames to the reply
        for people in people_to_tag:
            reply += "@" + people + " "

        random_reply = random.randint(0, 4)
        if random_reply == 0:
            reply += "\nDone!"
        elif random_reply == 1:
            reply += "\nGL!"

        reply = Bot.cash_app_tag(bot_info, text, reply)

        bot_info.api.update_status(reply, in_reply_to_status_id=tweet_id)
        print(reply)

    @staticmethod
    def cash_app(bot_info, text, user, tweet_id):
        if "tag" not in text:
            if "cashapp" in text or "cash app" in text or "cashtag" in text:
                reply = "@" + user.screen_name + "\n$" + bot_info.CASHAPP
                bot_info.api.update_status(reply, in_reply_to_status_id=tweet_id)

    @staticmethod
    def cash_app_tag(bot_info, text, reply):
        if "cashapp" in text or "cash app" in text or "cashtag" in text:
            reply += "\n$" + bot_info.CASHAPP

        return reply
