import tweepy
from tweepy.error import TweepError
import json
import glob
import dateutil.parser

api_key = 'jgKcJ535zMUd8H8yYibroFgFi'
api_secret = 'TxgRXsBVsPy2R6J26eMMqpuV8kM3GCHS3TM9ZRnLrlCT4z9f7W'

access_token = '1711405795-DyzMGIBehxXsCBnaipaCvdOtGMX79FWvq4yntx6'
access_token_secret = '07vqgbGf7oXfqLdKnjgbrLE06yWj7cIYAJdFW6MSXevrr'

file_dir = ''

date_min = dateutil.parser.parse('2020-01-11 00:00:00 +0000')
date_max = dateutil.parser.parse('2020-01-14 00:00:00 +0000')

print "Tweets between %s and %s will be deleted" % (date_min.isoformat(), date_max.isoformat())
print "Do you wish to continue? (y/n)"
choice = raw_input("> ")

if choice == 'y':
	auth = tweepy.OAuthHandler(api_key, api_secret)
	auth.set_access_token(access_token, access_token_secret)

	api = tweepy.API(auth)

	file_list = glob.glob(file_dir + '/*.js')
	file_list.sort()

	for file_name in file_list:
		print file_name
		f = open(file_name, 'r')
		f.readline() # clear the first junk line
		data = json.load(f);
		data.sort(key=lambda x: x['created_at'])

		for tweet in data:
			tweet_date = dateutil.parser.parse(tweet['created_at'])
			if tweet_date > date_min and tweet_date < date_max:
				print "-----------------------------------"
				print "%s: %s" % (tweet['created_at'], tweet['text'])
				try:
					api.destroy_status(tweet['id'])
					print "DELETED"
				except TweepError as te:
					print "ERROR %s" % te[0][0]['message']
			else:
				break
else:
	print "No tweets deleted"

print "Goodbye!"
