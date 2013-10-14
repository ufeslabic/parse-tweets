#!/usr/bin/env python
# -*- coding: utf-8 -*-
import csv, sys
from collections import defaultdict
from lib_cleaning import *
from lib_output import *
from lib_input import *
from lib_time import *


# adds a word to the dictionary of words and increment it's count
# if it's the first time this word is mentioned, it is inserted with count = 1
def handle_common_words(word, tweet_words, words, words_per_time, timestamp):
	lower_case_word = word.lower()
	clean_word = remove_punctuation(lower_case_word)
	if lower_case_word not in stopwords:
		words[clean_word] += 1
		if timestamp is not '':
			try:
				words_per_time[clean_word].append(timestamp)
			except KeyError:
				words_per_time[clean_word] = [timestamp]


# adds a URL to the hashtags dictionary and the username that tweeeted it
# if it's the first time this URL is tweeeted, it is inserted with only this username
def handle_urls(url, urls, username):	
	if len(url) in [22,23]: #checks if the URL wasn't truncated
		try:
			urls[url].add(username)
		except KeyError:
			# if the URL isn't in the URL's dict yet, adds it
			urls[url] = set([username])

# adds a hashtag to the hashtags dictionary and the username that mentioned it
# if it's the first time this hashtag is mentioned, it is inserted with only this username
def handle_hashtags(hashtag, hashtags, username):
	hashtag = remove_punctuation(hashtag)
	lower_case_hashtag = hashtag.lower()
	try:
		# adds the username to the set of usernames that commented on this hashtag
		hashtags[lower_case_hashtag].add(username)
	except KeyError:
		# if the hashtag isn't in the hashtags dict yet, adds it
		hashtags[lower_case_hashtag] = set([username])

# nothing is being done with mentions for now
def handle_mentions(profile_name, mentions, username):
	profile_name = remove_punctuation(profile_name)
	try:
		# adds the username to the set of usernames that commented on this hashtag
		mentions[profile_name].add(username)
	except KeyError:
		# if the hashtag isn't in the hashtags dict yet, adds it
		mentions[profile_name] = set([username])

# reads the words in the tweet and decides what to do with them		
def read_tweet_text(tweet_text, username, words, urls, hashtags, mentions, words_per_time, timestamp):	
	tweet_words = tweet_text.split()
	for word in tweet_words:
		if len(word) > 1:
			if word.startswith("http"):
				handle_urls(word, urls, username)
			else:				
				if word.startswith("#"):
					handle_hashtags(word, hashtags, username)
				elif word.startswith("@"):
					handle_mentions(word, mentions, username)
				else: #if the word isn't  hashtag, mention or URL it is a common word
					handle_common_words(word, tweet_words, words, words_per_time, timestamp)					

		
# the input file is set to 'tweets_FIXED' because it is the output of remove_null_byte
def main(input_file='tweets_FIXED.csv', delimiter='|', output_type='csv'):

	# dictionary of URLS where each entry contains a set of distinct usernames that tweeted this URL
	urls = {}
	# entry example: 'http://www.google.com' => ['Mary','John','Ronaldo']

	# dictionary of hashtags where each entry contains a set of distinct usernames that commented on this hashtag
	hashtags = {}
	# entry example: 'chocolate' => ['johnDoe85','barack0','_b0btables', ...]

	# dictionary of mentions where each entry contains a set of distinct usernames that commented on this hashtag
	mentions = {}
	# entry example: 'uFulano2128_' => ['johnDoe85','barack0','_b0btables', ...]

	# dictionary of users where each entry contains their geo-coordinates, up to one per user
	users_position = {}
	# entry example: 'random_Person' => (latitude,longitude)

	# dictionary of users where each entry contains their geo-coordinates, up to one per user
	users = defaultdict(int)
	# entry example: 'random_Person' => (latitude,longitude)

	# dictionary of words where each entry contains the times they were mentioned	
	words = defaultdict(int)
	# entry example: 'chocolate' => 9001

	# dictionary of the number of tweets per day
	dates = defaultdict(int)
	# entry example: '02/08/2013' => 1234	

	# dictionary of words where each entry contains the times they were mentioned	
	tweets_count = defaultdict(int)
	# entry example: 'chocolate' => 9001

	# variables for the timeline
	timestamp_list =[]
	words_per_time = {}	
	number_of_topwords = options_parser(sys.argv)['number_of_words']
	
	line_num = 0
	remove_null_byte()

	with open(input_file, 'rt', encoding="utf8") as csvfile:
		try:
			csv_in = csv.reader(csvfile, delimiter=delimiter, quotechar='"')		
			for line in csv_in:			
				tweet_text = line[0]
				tweets_count[tweet_text] += 1
				username = line[2]
				users[username] += 1
				try:					
					timestamp = line[12]
					if timestamp:
						dates[datetime.datetime.fromtimestamp(int(timestamp)).strftime('%d/%m/%Y')] += 1
						timestamp = datetime.datetime.fromtimestamp(int(timestamp))
						timestamp_list.append(timestamp)
				except:
					timestamp = ''						

				# lines where the eighth column is 'Point' have geographical data
				try:
					if line[8] == 'Point':
						users_position[username] = (line[9],line[10])
				except: 
					pass #if the tweet doesn't have geocoordinates 
				
				read_tweet_text(tweet_text, username, words, urls, hashtags, mentions,words_per_time, timestamp)
				line_num = line_num + 1

		except UnicodeDecodeError:
				print(line)
				error_parsing(line_num)
		except IndexError:
				print("Erro na linha:" + str(line_num))

	for key, list_of_users in hashtags.items():
		hashtags[key] = len(list_of_users)

	for key, list_of_users in mentions.items():
		mentions[key] = len(list_of_users)
	
	locations_to_csv(users_position)

	top_something_to_csv(urls, 'urls.csv', ['urls', 'distinct_users'], True, sort_key=lambda t: t[1], value_format=lambda t: len(t))
	top_something_to_csv(dates, 'dates.csv', ['date', 'number_of_tweets'], reverse=False, sort_key=lambda t: datetime.date(int(t[0][6:]), int(t[0][3:5]), int(t[0][:2])))
	top_something_to_csv(hashtags, 'hashtags.csv', ['hashtags', 'distinct_users_commenting'], True, sort_key=lambda t: t[1], value_format=lambda t:t)
	top_something_to_csv(mentions, 'mentions.csv', ['mentions', 'distinct_users_mentioning'], True, sort_key=lambda t: t[1], value_format=lambda t:t)
	top_something_to_csv(users, 'users_activity.csv', ['user', 'total_tweets'], True, sort_key=lambda t: t[1], value_format=lambda t:t)
	top_something_to_csv(tweets_count, 'top_tweets.csv', ['tweet', 'times_tweeted'], True, sort_key=lambda t: t[1], value_format=lambda t:t)
	dict_to_txt_for_wordle(words, 'top_words_wordle.txt', sort_key=lambda t:t[1])
	dict_to_txt_for_wordle(hashtags, 'top_hashtags_wordle.txt', sort_key=lambda t: t[1])
	timeline(words_per_time, get_N_first(words, number_of_topwords), timestamp_list)
	cleanup()

if __name__ == '__main__':	
	main()
