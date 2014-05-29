#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This module defines some functions used to output the results of the script.
The constants used in it are:
	* MAX_WORDS_NUMBER_CSV: maximum number of words to be present in 
	the top_words.csv file;
	* MAX_WORDS_NUMBER_WORDCLOUD: maximum number of words to be in the TXT
	file that will be used to generate the wordcloud;
"""
import csv
import sys

DEFAULT_OUTPUT_DELIMITER = '|'

MAX_WORDS_NUMBER_CSV = 1000
MAX_WORDS_NUMBER_WORDCLOUD = 120

def normalize_dict(dict_str_int_wordcount):
	""" 
	Normalize the dictionary with the word count to generate the wordcloud.
	Normalizing, in this function, is give the most recurring word the value 100 and give
	all the other values proportional to it.
	"""
	max_elem = max(dict_str_int_wordcount.values())	
	for key, value in dict_str_int_wordcount.items():
		normalized_val = float((100 * value)/max_elem)
		if normalized_val < 1:
			normalized_val = 1
		dict_str_int_wordcount[key]= normalized_val		
	return dict_str_int_wordcount


def dict_to_txt_for_wordle(dict_str_int_wordcount, filename, sort_key=lambda t:t, value_key=lambda t:t):
	"""
	Writes the normalized dict in a txt to be pasted manually 
	in wordle.net or another wordcloud service
	Entries in the dict_str_int_wordcount dictionary are in the format "string_word => integer_count"
	i.e.: "chocolate => 10000"
	"""
	if not dict_str_int_wordcount:
		dict_str_int_wordcount = {'No hashtags found': 1}
	ordered_list = []
	dict_str_int_wordcount = normalize_dict(dict_str_int_wordcount)
	for key, value in dict_str_int_wordcount.items():
		ordered_list.append([key, value_key(value)])	
	ordered_list = 	sorted(ordered_list, key=sort_key, reverse=True)	
	out = open(filename, 'w', encoding= 'utf-8')
	for item in ordered_list[:MAX_WORDS_NUMBER_WORDCLOUD]:		
		i = 0
		while i < int(item[1]):
			out.write(item[0] + ' ')
			i+=1	
	out.close()

def locations_to_csv(dict_str_tuple, filename='locations.csv'):
	"""
	Creates a CSV file of the latitude and longitude data of the tweets
	param: dict_str_tuple is a dictionary where each entry is in 
	the format "string_username => ('latitude', 'longitute')
	i.e: ronald0 => ('0.012081210', '0.9121218298172')
	"""
	with open(filename, 'w', newline='', encoding="utf8") as csvfile:
		file_writer = csv.writer(csvfile, delimiter=DEFAULT_OUTPUT_DELIMITER, quotechar='"', quoting=csv.QUOTE_MINIMAL)
		file_writer.writerow(['latitude', 'longitute'])
		for key, value in dict_str_tuple.items():
			file_writer.writerow([value[0], value[1]])
		csvfile.close()

def top_something_to_csv(dict_in, filename, column_titles, reverse, sort_key_function, value_format_function=lambda t: t):
	"""
	Given a dictionary, a sorting function for it's keys
	a value format function to format the output, this function generates
	a CSV file with the ordered by the keys with the key as the first column 
	and the value as the second. The file can be ordered in reverse.
	"""
	ordered_list = []
	for key, value in dict_in.items():
		ordered_list.append([key, value_format_function(value)])

	ordered_list = sorted(ordered_list, key=sort_key_function, reverse=reverse)

	with open(filename, 'w', newline='', encoding="utf8") as csvfile:
		file_writer = csv.writer(csvfile, delimiter=DEFAULT_OUTPUT_DELIMITER, quotechar='"', quoting=csv.QUOTE_MINIMAL)	
		file_writer.writerow(column_titles)
		for item in ordered_list[:MAX_WORDS_NUMBER_CSV]:
			file_writer.writerow([item[0], item[1]])
		csvfile.close()	

def top_something_to_csv_with_relations(filename, dict_in, dict_usernames_relations, column_titles):
	"""
	Given a dictionary of usernames and an integer metric quantity about them	
	a CSV file with the ordered by the keys with the key as the first column 
	and the value as the second. The resulting file has the columns:
	username, metric_value, followers_count, friends_count
	"""
	ordered_list = []
	for key, value in dict_in.items():
		ordered_list.append([key, value])
	ordered_list = sorted(ordered_list, key=lambda t: t[1], reverse=True)

	with open(filename, 'w', newline='', encoding="utf8") as csvfile:
		file_writer = csv.writer(csvfile, delimiter=DEFAULT_OUTPUT_DELIMITER, quotechar='"', quoting=csv.QUOTE_MINIMAL)	
		file_writer.writerow(column_titles)
		for item in ordered_list[:MAX_WORDS_NUMBER_CSV]:
			username = item[0]
			try:			
				followers_count = dict_usernames_relations[username][0]
				friends_count = dict_usernames_relations[username][1]
			except:
				followers_count = '-'
				friends_count = '-'
			file_writer.writerow([username, item[1], followers_count, friends_count])
		csvfile.close()

def error_parsing(line_num):
	""" Returns an error message with the corrupted text and exits the program."""
	print("Error on line: "+ str(line_num))	
	print("Error: Not all tweeted were read. Finishing execution...")
	sys.exit()

# write a set to CSV
def write_set_of_tuples(set_tup_input, filename, column_titles):
	with open(filename, 'w', newline='', encoding="utf8") as csvfile:
		file_writer = csv.writer(csvfile, delimiter=DEFAULT_OUTPUT_DELIMITER, quotechar='"', quoting=csv.QUOTE_MINIMAL)
		file_writer.writerow(column_titles)
		for element in set_tup_input:
			file_writer.writerow(list(element))





