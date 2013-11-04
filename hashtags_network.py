#!/usr/bin/env python
# -*- coding: utf-8 -*-
import csv, itertools
from lib_cleaning import *

def read_hashtags(tweet, timestamp):
	list_str_words = tweet.split()
	list_str_hashtags = []
	for word in list_str_words:
		if word.startswith("#") and not(word.endswith("…")):
			temp_word = remove_punctuation(word.lower())
			if len(temp_word) > 1:
				list_str_hashtags.append("#"+temp_word)
	with open('hashtags_network.csv', 'a', encoding="utf8") as csvfile:			
		file_writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
		for item in itertools.combinations(list_str_hashtags, 2):
			file_writer.writerow([item[0], item[1], timestamp])
			

	






