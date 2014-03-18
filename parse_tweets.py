#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv
import sys
from collections import defaultdict

from hashtags_network import hashtags_relations_to_csv
from hashtags_network import process_hashtags_relations
from lib_file_fixing import file_fix
from lib_input import DEFAULT_INPUT_DELIMITER, cleanup, get_cluster_usernames 
from lib_input import options_parser
from lib_output import top_something_to_csv, locations_to_csv
from lib_output import dict_to_txt_for_wordle, locations_to_csv, write_tweets_with_links
from lib_text import remove_invalid_characters, is_stopword, is_hashtag, is_URL
from lib_text import is_twitter_mention, is_valid_twitter_short_url, remove_latin_accents
from lib_text import remove_punctuation, has_links

from lib_time import *

def handle_urls(str_url, dict_set_urls, str_username):
	"""
	Adds a URL to the URLS dictionary. Each entry contains a set of 
	users that tweeted the key URL.
	"""	
	if is_valid_twitter_short_url(str_url):
		try:
			dict_set_urls[str_url].add(str_username)
		except KeyError:
			dict_set_urls[str_url] = set([str_username])

def handle_hashtags(str_hashtag, dict_set_hashtags, str_username):
	"""
	Adds a hashtag to the hashtags dictionary. Each entry contains a set of 
	users that tweeted the key hashtag.
	"""
	str_hashtag = str_hashtag.lower()
	str_hashtag = remove_punctuation(str_hashtag)
	if str_hashtag is not '':
		try:
			dict_set_hashtags[str_hashtag].add(str_username)
		except KeyError:
			dict_set_hashtags[str_hashtag] = set([str_username])

def handle_mentions(str_mentioned_username, dict_set_mentions, str_username_that_mentioned):
	"""
	Adds a mention to the mentions dictionary. Each entry contains a set of 
	users that mentioned the key profile.
	"""
	str_mentioned_username = str_mentioned_username.lower()
	str_mentioned_username = remove_punctuation(str_mentioned_username)
	if str_mentioned_username is not '':
		#str_mentioned_username = str_mentioned_username.lower()
		try:
			dict_set_mentions[str_mentioned_username].add(str_username_that_mentioned)
		except KeyError:
			dict_set_mentions[str_mentioned_username] = set([str_username_that_mentioned])

def handle_common_words(str_word, dict_int_words):
	""" 
	Inserts a word in the dictionary of word counts or increment the 
	count if it already was used. 
	"""
	str_word = str_word.lower()
	str_word = remove_punctuation(str_word)
	if str_word is not '':		
		#after the word was cleaned, it may have 0 letters i.e: if the word was ";)"
		if (not is_stopword(str_word)) and len(str_word) > 1:
			dict_int_words[str_word] += 1
	
# part of the new feature, not yet finished	
def count_users_by_date(dict_int_users_by_date, str_date, str_username):
	"""
	Adds a date to the dates dictionary and the usernames that 
	tweeeted on this date.
	"""
	try:
		dict_int_users_by_date[str_date].add(str_username)
	except KeyError:
		dict_int_users_by_date[str_date] = set([str_username])

# part of the new feature, not yet finished
def add_word_to_timeline(str_word, words_per_time, timestamp):
	if timestamp is not '':
		str_word = remove_punctuation(str_word)
		if str_word is not None:
			str_word = str_word.lower()
			if (not is_stopword(str_word)) and len(str_word) > 1:
				try:
					words_per_time[str_word].append(timestamp)
				except KeyError:
					words_per_time[str_word] = [timestamp]

def read_tweet_text(tweet_text, str_username, words, dict_set_urls, dict_set_hashtags, 
	dict_set_mentions, words_per_time, timestamp):
	"""
	Reads each string in a tweet. If a string isn't an URL, a mention 
	or a hashtag it can be a smiley face, pure punctuation or 
	just a regular word.
	About this function signature and others around here...yes, we know python can look in the "above" function namespace 
	to find a variable, but it is more human friendly this way.
	"""
	tweet_words = tweet_text.split()
	for str_word in tweet_words:
		if len(str_word) > 1 and not str_word.endswith('…'): # if it ends in '…' the tweet was truncated by YTK
			if is_URL(str_word):
				handle_urls(str_word, dict_set_urls, str_username)
			elif is_hashtag(str_word):
				handle_hashtags(str_word, dict_set_hashtags, str_username)
			elif is_twitter_mention(str_word):
				handle_mentions(str_word, dict_set_mentions, str_username)
			else:
				handle_common_words(str_word, words)
				add_word_to_timeline(str_word, words_per_time, timestamp)

def main(input_file='tweets_FIXED_NO_DUPLICATES.csv'):
	"""
	Input file is set to 'tweets_FIXED' because it is the output of remove_null_byte()
	"""
	file_fix('tweets.csv')
	list_cluster_usernames = get_cluster_usernames()
	terminal_options = options_parser(sys.argv)
	
	# Dictionary of URLS where each entry contains a set of distinct 
	# usernames that tweeted this URL.
	# Entry example: 'http://www.google.com' => ['Mary','John','Ronaldo']	
	dict_set_urls = {}

	# Dictionary of hashtags where each entry contains a set of distinct
	#usernames that commented on this hashtag.
	# entry example: 'chocolate' => ['johnDoe85','barack0','_b0btables', ...]
	dict_set_hashtags = {}	

	# Dictionary of mentions where each entry contains a set of distinct 
	# usernames that mentioned a profile.
	# Entry example: 'uFulano2128_' => ['johnDoe85','barack0','_b0btables', ...]
	dict_set_mentions = {}

	# Dictionary of users where each entry contains their last given geo-coordinates
	# Entry example: 'random_Person' => (latitude,longitude)
	dict_tuple_users_positions = {}

	# Dictionary of distinct usernames by date.
	# Entry example: '04/05/2013' => ['ronaLDO', 'Rivaldo', 'RobertoCarlos_']
	dict_int_users_by_date = {}
	
	# Dictionary of words where each entry contains the number of times 
	# they were mentioned.
	# Entry example: 'chocolate' => 9001
	dict_int_words = defaultdict(int)
	
	# Dictionary with the number of tweets in a given date. 
	# entry example: '02/08/2013' => 1234
	dates = defaultdict(int)

	# Dictionary with the number of distinct users that tweeted a hashtag. 
	# entry example: 'beliebers' => 12
	dict_int_hashtags = defaultdict(int)

	# Dictionary with the number of distinct users that mentioned a profile. 
	# entry example: '0bama' => 789
	dict_int_mentions = defaultdict(int)

	# Dictionary with the number of tweets by a user. 
	# entry example: 'ronald0' => 11
	dict_int_users_activity = defaultdict(int)

	# Dictionary with the tweet texts. 
	# entry example: 'a nice tweet example #creativity' => 11
	tweets_count = defaultdict(int)

	# List with hashtags relations tuples
	# entry example: (#salt, #pepper)
	list_tuple_hashtags_relations = []

	# counter for the number of incorrect timestamps in a dataset
	int_incorrect_timestamps = 0

	# counter for the number of corrupted lines
	int_corrupted_lines = 0
	
	# The "Words timeline" feature is finished nor documented.
	timestamp_list =[]
	words_per_time = {}	
	number_of_topwords = terminal_options['number_of_words']

	# Dictionary of tweets that have links
	set_tup_str_tweets_with_links = set()
	
	with open(input_file, 'rt', encoding="utf8") as csvfile:
		try:
			csv_in = csv.reader(csvfile, delimiter=DEFAULT_INPUT_DELIMITER, quoting=csv.QUOTE_NONE)
			lis_column_titles = next(csv_in) #Skips the line with the column titles.
			try:
				for line in csv_in:
					if len(line) is 13:
						if has_links(line[0]):							
							set_tup_str_tweets_with_links.add(tuple(line))
						str_username = line[2]
						str_username = str_username.lower()
						if (not list_cluster_usernames) or (str_username in list_cluster_usernames):
							tweet_text = line[0]
							tweets_count[tweet_text] += 1
							dict_int_users_activity[str_username] += 1
							try:
								# Sometimes this data is corrupted by YourTwapperKeeper,
								# this is why this clause is in a "try" block.
								timestamp = line[12]
								
								# Append the relations between the hashtags found in the tweet to a list
								list_tuple_hashtags_relations += process_hashtags_relations(tweet_text)
								if timestamp:
									str_date = datetime.datetime.fromtimestamp(int(timestamp)).strftime('%d/%m/%Y') # date STRING in the format DD/MM/YYYY
									count_users_by_date(dict_int_users_by_date, str_date, str_username)
									dates[datetime.datetime.fromtimestamp(int(timestamp)).strftime('%d/%m/%Y')] += 1
									timestamp = datetime.datetime.fromtimestamp(int(timestamp))
									timestamp_list.append(timestamp)
							except ValueError:
								timestamp = ''
								int_incorrect_timestamps += 1
							# Lines where the eighth column is 'Point' have 
							# geographical data on columns 9(latitude) and 10(longitute).
							# Sometimes this data is corrupted by YourTwapperKeeper,
							# this is why this clause is in a "try" block.
							if line[8] == 'Point':					
								dict_tuple_users_positions[str_username] = (line[9],line[10])

							read_tweet_text(tweet_text, str_username, dict_int_words, dict_set_urls, dict_set_hashtags, dict_set_mentions,words_per_time, timestamp)
					else:
						int_corrupted_lines += 1
			
			except (UnicodeDecodeError, IndexError):
				print(line)
				error_parsing(csv_in.line_num)

		except (IOError, StopIteration):
			print("Error opening some necessary files.")
			print("Make sure you have a 'tweets.csv' file in this folder.")
			print("Please ensure that you are not running the script as root.")

		int_total_line_num = csv_in.line_num		

	# Sets the hashtag dict entry count as the length of the set of different users that tweeted it.
	for key, list_of_users in dict_set_hashtags.items():
		dict_int_hashtags[key] = len(list_of_users)

	# Sets the mention count as the length of the set of different users that mentioned it.
	for key, list_of_users in dict_set_mentions.items():
		dict_int_mentions[key] = len(list_of_users)
	
	# Writing the CSV's of all that was calculated.
	locations_to_csv(dict_tuple_users_positions)
	
	hashtags_relations_to_csv(list_tuple_hashtags_relations)
	
	top_something_to_csv(dict_set_urls, 'top_urls.csv', ['urls', 'distinct_users'], 
		reverse=True, 
		sort_key_function=lambda t: t[1], 
		value_format_function=lambda t: len(t))
	
	top_something_to_csv(dict_int_users_by_date, 'users_by_date.csv', ['date', 'distinct_users'], 
		reverse=False, 
		sort_key_function=lambda t:(t[0:2], t[3:5], t[6:8]), 
		value_format_function=lambda t: len(t))
	
	top_something_to_csv(dates, 'dates.csv', ['date', 'number_of_tweets'], 
		reverse=False, 
		sort_key_function=lambda t: datetime.date(int(t[0][6:]), int(t[0][3:5]), int(t[0][:2])))
	
	top_something_to_csv(dict_int_hashtags, 'hashtags.csv', ['hashtags', 'distinct_users_commenting'], 
		reverse=True, 
		sort_key_function=lambda t: t[1], 
		value_format_function=lambda t:t)
	
	top_something_to_csv(dict_int_mentions, 'mentions.csv', ['mentions', 'distinct_users_mentioning'], 
		reverse=True, 
		sort_key_function=lambda t: t[1], 
		value_format_function=lambda t:t)	
	
	top_something_to_csv(dict_int_users_activity, 'users_activity.csv', ['user', 'total_tweets'], 
		reverse=True, 
		sort_key_function=lambda t: t[1], 
		value_format_function=lambda t:t)
	
	top_something_to_csv(tweets_count, 'top_tweets.csv', ['tweet', 'times_tweeted'], 
		reverse=True, 
		sort_key_function=lambda t: t[1], 
		value_format_function=lambda t:t)
	
	top_something_to_csv(dict_int_words, 'top_words.csv', ['word', 'times_mentioned'], 
		reverse=True, 
		sort_key_function=lambda t: t[1], 
		value_format_function=lambda t:t)

	# Writing the TXT's files of the wordclouds.
	dict_to_txt_for_wordle(dict_int_words, 'top_words_wordle.txt', sort_key=lambda t:t[1])
	dict_to_txt_for_wordle(dict_int_hashtags, 'top_hashtags_wordle.txt', sort_key=lambda t: t[1])

	# Writing the word timeline.
	timeline(words_per_time, get_N_first(dict_int_words, number_of_topwords), timestamp_list)

	# Writing tweets that have links
	write_tweets_with_links(set_tup_str_tweets_with_links, 'tweets_with_links.csv', column_titles=lis_column_titles)
	
	print(str(int_total_line_num) + "\t lines read.")
	print(str(len(dict_tuple_users_positions.keys())) + "\t lweets with geolocation data.")
	print(str(int_corrupted_lines) + "\t corrupted lines in this dataset.")	

	cleanup()	

if __name__ == '__main__':
	main()
