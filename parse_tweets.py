#!/usr/bin/env python
# -*- coding: utf-8 -*-

from collections import defaultdict
import csv, sys, datetime
import os.path

from lib_cleaning import *
from lib_output import *
from lib_input import *

# read a tweet's text counting words, hashtags and links
def parse_tweet(tweet_text, username, words, urls, hashtags):	
	for word in tweet_text.split():
		if word.startswith("#"):	
			hashtag = remove_punctuaction(word).lower()
			try:
				users_by_hashtag = hashtags[hashtag]
				if username not in users_by_hashtag:				
					hashtags[hashtag].append(username)
			except KeyError:
				hashtags[hashtag] = [username]
		else:
			if len(word) > 1:
				#TODO shortlink length size varies with time on twitter, get this from their configuration
				if (word.startswith('http')) and (len(word) in [22,23]):
					try:
						users_that_tweeted = urls[word]
						if username not in users_that_tweeted:
							urls[word].append(username)
					except KeyError:
						urls[word] = [username]
				else:			
					word = ''.join(character for character in word if character not in weird_characters)
					word = remove_punctuaction(word).lower()
					if word not in stopwords:
						words[word] += 1


def main(input_file='tweets.csv', delimiter='|', output_type='csv'):
	urls = {}
	words = defaultdict(int)		
	hashtags = {}
	dates = defaultdict(int)
	users_position = {}

	with open(input_file, 'rt', encoding="utf8") as csvfile:
		csv_in = csv.reader(csvfile, delimiter=delimiter, quotechar='"')
		for line in csv_in:			
			tweet_text = line[0]
			username = line[2]
			try:
				timestamp = line[12]
				if timestamp:
					dates[datetime.datetime.fromtimestamp(int(timestamp)).strftime('%d/%m/%Y')] += 1
			except:
				pass
			# lines where the eighth column is 'Point' have geographical data
			try:
				if line[8] == 'Point':
					users_position[username] = (line[9],line[10])
			except:
				pass
			parse_tweet(tweet_text, username, words, urls, hashtags)
	
	for key, list_of_users in hashtags.items():
		hashtags[key] = len(list_of_users)
	
	locations_to_csv(users_position)	
	top_something_to_csv(urls, 'urls.csv', ['urls', 'distinct_users'], True, sort_key=lambda t: t[1], value_format=lambda t: len(t))
	top_something_to_csv(dates, 'dates.csv', ['date', 'distinct_users_by_date'], reverse=False, sort_key=lambda t: datetime.date(int(t[0][6:]), int(t[0][3:5]), int(t[0][:2])))
	top_something_to_csv(hashtags, 'hashtags.csv', ['hashtags', 'distinct_users_commenting'], True, sort_key=lambda t: t[1], value_format=lambda t:t)		
	dict_to_txt_for_wordle(words, 'top_words_wordle.txt', sort_key=lambda t:t[1])
	dict_to_txt_for_wordle(hashtags, 'top_hashtags_wordle.txt', sort_key=lambda t: t[1])#	top_dates_to_csv(top_dates)

if __name__ == '__main__':	
	main()
