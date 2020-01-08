import tweepy, time, sys, datetime, random

class Bot:
    def RunMainBot(self, botInfo):
        print("\nRUNNING MAIN BOT-----------------", datetime.datetime.now().strftime("%H:%M:%S"))
        while botInfo.run_loop == True:
            display_counter = 1
            new_tweet_counter = 0

            for current_search in botInfo.search_words:
                filtered_search = current_search + " -filter:retweets-filter:replies"
                overflow_count = 0
                current_search_counter = 0
                already_liked_counter = 0
                already_retweeted_counter = 0

                print("\n--Search #", display_counter,"--", datetime.datetime.now().strftime("%H:%M:%S"))

                follower_count = botInfo.api.get_user(botInfo.USERNAME).followers_count
                botInfo.run_loop = self.CheckFollowerCount(botInfo, follower_count)

                if botInfo.run_loop == False:
                    break

                while current_search_counter < botInfo.TWEET_LIMIT_PER_SEARCH and overflow_count <= botInfo.OVERFLOW_SEARCH_REPEAT:
                    if overflow_count != 0:
                        print("Overflow Mode----")
                        time.sleep(5)

                    #grabs all the tweets and decides whether or not to like, retweet, or follow them
                    for tweet in tweepy.Cursor(botInfo.api.search, q=filtered_search, lang="en", since=botInfo.date_since, tweet_mode = "extended").items(botInfo.TWEET_SEARCH_LIMIT + (overflow_count * botInfo.OVERFLOW_EXTRA_SEARCHES)):
                        if current_search_counter > botInfo.TWEET_LIMIT_PER_SEARCH:
                            print("Tweet limit reached for search")
                            break

                        user = tweet.user
                        id = tweet.id
                        url = 'https://twitter.com/' + user.screen_name +  '/status/' + str(id)
                        text = tweet.full_text.lower()

                        #checks the tweet for any competition rules that can't work with this bot
                        tweet_passes_filter = True
                        for word_filter in botInfo.filtered_words:
                            if word_filter in text:
                                tweet_passes_filter = False

                        #check for bot spotters or other annoying users
                        for user_filter in botInfo.filtered_users:
                            if user_filter in user.screen_name.lower():
                                tweet_passes_filter = False
                                print("\tBot Spotter avoided: " + user.screen_name)

                        #only likes, retweets, or follows if the tweet passes all the filters
                        if tweet_passes_filter == True:
                            retweet_status = self.Retweet(botInfo, tweet, text)
                            #self.Tag(botInfo, tweet, text, user)
                            if retweet_status != 0:
                                self.Follow(botInfo, tweet, text, user)
                                like_status = self.Like(tweet, text)
                                current_search_counter += 1
                                new_tweet_counter += 1

                                if like_status == 2:
                                    already_liked_counter += 1
                            else:
                                already_retweeted_counter += 1

                    overflow_count += 1

                    if current_search_counter == 0:
                        print("\tAll tweets failed filter!")
                    else:
                        print("\tAlready Retweeted: ", already_retweeted_counter)
                        print("\tAlready Liked: ", already_liked_counter)
                        print("\tCurrent Search - New Tweets: ", current_search_counter)
                    if current_search_counter == None:
                        print("ERROR: TWEET COUNTER = NONE")

                display_counter += 1

            print("\nCurrent Run Finished----")
            print ("Time: ", datetime.datetime.now().strftime("%H:%M:%S"))
            print ("New Tweets: ", new_tweet_counter)
            print ("Total Tweets: ", botInfo.total_tweets_since_start)
            time.sleep(botInfo.SEARCH_TIMER)

    def RunLikeRetweetOnlyBot(self, botInfo):
        print("\nRUNNING IN LIKE AND RETWEET ONLY MODE--------------", datetime.datetime.now().strftime("%H:%M:%S"))
        custom_filtered_words = botInfo.filtered_words + ["follow"]
        switch_counter = 0

        time.sleep(10)
        while botInfo.run_loop == True:
            display_counter = 1
            new_tweet_counter = 0

            if switch_counter >= botInfo.RUNS_BEFORE_SWITCH:
                self.RunMainBot(botInfo)

            #runs through all custom searches and finds tweets within this search
            for current_search in botInfo.search_words:
                filtered_search = current_search + " -filter:retweets-filter:replies"
                overflow_count = 0
                current_search_counter = 0
                already_liked_counter = 0
                already_retweeted_counter = 0

                print("\n--Search #", display_counter,"--", datetime.datetime.now().strftime("%H:%M:%S"))

                while current_search_counter < botInfo.TWEET_LIMIT_PER_SEARCH and overflow_count <= botInfo.OVERFLOW_SEARCH_REPEAT:
                    if overflow_count != 0:
                        print("Overflow Mode----")
                        time.sleep(5)

                    #grabs all the tweets and decides whether or not to like or retweet (following has been removed)
                    for tweet in tweepy.Cursor(botInfo.api.search, q=filtered_search, lang="en", since=botInfo.date_since, tweet_mode = "extended").items(botInfo.TWEET_SEARCH_LIMIT + (overflow_count * botInfo.OVERFLOW_EXTRA_SEARCHES)):
                        if current_search_counter > botInfo.TWEET_LIMIT_PER_SEARCH:
                            print("Tweet limit reached for search")
                            break

                        user = tweet.user
                        id = tweet.id
                        url = 'https://twitter.com/' + user.screen_name +  '/status/' + str(id)

                        try:
                            text = tweet.retweeted_status.full_text.lower()
                        except:
                            text = tweet.full_text.lower()

                        #checks the tweet for any competition rules that can't work with this bot
                        tweet_passes_filter = True
                        for word_filter in botInfo.filtered_words:
                            if word_filter in text:
                                tweet_passes_filter = False

                        #check for bot spotters or other annoying users
                        for user_filter in botInfo.filtered_users:
                            if user_filter in user.screen_name.lower():
                                tweet_passes_filter = False
                                print("\tBot Spotter avoided: " + user.screen_name)

                        #only likes or retweets if the tweet passes all the filters
                        if tweet_passes_filter == True:
                            retweet_status = self.Retweet(botInfo, tweet, text)
                            #self.Tag(botInfo, tweet, text, user)
                            if retweet_status != 0:
                                like_status = self.Like(tweet, text)
                                current_search_counter += 1
                                new_tweet_counter += 1

                                if like_status == 2:
                                    already_liked_counter += 1
                            else:
                                already_retweeted_counter += 1

                    overflow_count += 1

                    if current_search_counter == 0:
                        print("\tAll tweets failed filter!")
                    else:
                        print("\tAlready Retweeted: ", already_retweeted_counter)
                        print("\tAlready Liked: ", already_liked_counter)
                        print("\tCurrent Search - New Tweets: ", current_search_counter)
                    if current_search_counter == None:
                        print("ERROR: TWEET COUNTER = NONE")

                display_counter += 1

            switch_counter += 1
            print("\nCurrent Run Finished----")
            print ("Time: ", datetime.datetime.now().strftime("%H:%M:%S"))
            print ("New Tweets: ", new_tweet_counter)
            print ("Total Tweets: ", botInfo.total_tweets_since_start)
            time.sleep(botInfo.LIKE_RETWEET_ONLY_TIMER)

    def CheckFollowerCount(self, botInfo, follower_count):
        #checks follower count to remove followers if over limit
        if(follower_count >= botInfo.FOLLOWER_LIMIT):
            followers_list = botInfo.api.followers("NormanRoss04")
            for i in range(50):
                try:
                    botInfo.api.destroy_friendship(followers_list[i])
                except tweepy.TweepError as e:
                    print("ERROR unfollowing")
                    print(e)
                    return False
        return True

    def Like(self, tweet, text):
        if "like" in text or "fav" in text:
            try:
                tweet.favorite()
                print('\tLiked')
                return 1
            except tweepy.TweepError as e:
                return 2
        return 0

    def Retweet(self, botInfo, tweet, text):
        if "retweet" in text or "rt" in text:
            if not tweet.retweeted:
                try:
                    tweet.retweet()
                    print("\tRetweeted")
                    botInfo.total_tweets_since_start += 1
                    return 1
                except tweepy.TweepError as e:
                    return 0
        return 0

    def Follow(self, botInfo, tweet, text, user):
        if "follow" in text:
            try:
                to_follow = [user.screen_name] + [i['screen_name'] for i in tweet.entities['user_mentions']]

                for screen_name in list(set(to_follow)):
                    botInfo.api.create_friendship(screen_name)
                    print('\t' + "Followed: " + screen_name)

            except tweepy.TweepError as e:
               if("161" in e.response.text):
                   print("Follow limit reached!")
                   self.RunLikeRetweetOnlyBot(botInfo)
               else:
                   print(e)
                   print("ERROR Following")
        blah = 0

    def Tag(self, botInfo, tweet, text, user):
        followers_list = botInfo.api.followers(user)

        if "tag" in text:
            people_to_tag = []
            print("TAG FOUND")
            if "1" in text or "one" in text:
                people_to_tag += [followers_list[0]]
                self.Tag_People(botInfo, user, people_to_tag, 1)
            elif "2" in text or "two" in text:
                people_to_tag += [followers_list[0]] + [followers_list[1]]
                self.Tag_People(botInfo, user, people_to_tag, 2)
            elif "3" in text or "three" in text:
                people_to_tag += [followers_list[0]] + [followers_list[1]] + [followers_list[2]]
                self.Tag_People(botInfo, user, people_to_tag, 3)

    def Tag_People(self, botInfo, user, people_to_tag, number):
        reply = "@" + user.screen_name
        for people in people_to_tag:
            reply += " " + people.screen_name

        random_reply = random.randint(0,1)
        if random_reply == 0:
            reply += "\n Done!"
        else:
            reply += "\n GL!"

        print(reply)
