#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This module contains the necessary functions to parse the hashtags
in a tweet, creates combinations of them and outputs a list of relations.
It is an experimental feature.
"""
import csv
import itertools
from lib_text import remove_invalid_characters, remove_punctuation
from lib_output import DEFAULT_OUTPUT_DELIMITER

GEPHI_DELIMITER=';'

def get_hashtags(str_text):
	""" 
	Returns all the hashtags in a given string. 
	Hashtags are considered words that start with # and 
	have a length bigger than 1, not considering the # character. 
	"""
	list_str_words = str_text.split()
	list_str_hashtags = []
	for word in list_str_words:
		if word.startswith("#") and not(word.endswith("…")): #checks if the word wasn't truncated by YTK
			temp_word = remove_punctuation(word.lower())
			if temp_word is not None and len(temp_word) > 1:
				list_str_hashtags.append("#" + temp_word)
	return list_str_hashtags

def process_hashtags_relations(str_tweet_text):
	""" Returns all the tuples of combinations of hashtags in a tweet. """
	list_str_hashtags = get_hashtags(str_tweet_text)
	list_hashtags_combinations = []
	for item in itertools.combinations(list_str_hashtags, 2):
		list_hashtags_combinations.append([item[0], item[1]])	
	return(list_hashtags_combinations)

def hashtags_relations_to_csv(list_tuple_hashtags, filename='hashtags_network.csv'):	
	"""
	Generates a file to be used by Gephi to create a graph of 
	the relations between the hashtags.	
	"""	
	with open(filename, 'w', newline='', encoding="utf8") as csvfile:		
		file_writer = csv.writer(csvfile, delimiter=GEPHI_DELIMITER, quotechar='"', quoting=csv.QUOTE_MINIMAL)
		file_writer.writerow(['source', 'target'])
		for hashtag_tuple in list_tuple_hashtags:
			file_writer.writerow([hashtag_tuple[0], hashtag_tuple[1]])
		csvfile.close()

	
			

	






