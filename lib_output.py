#!/usr/bin/env python
# -*- coding: utf-8 -*-
import csv, sys

# normalize the dictionary with the word count to generate the wordcloud
def normalize_dict(dic):
	max_elem = max(dic.values())
	for key, value in dic.items():
		normalized_val = int((100 * value)/max_elem)
		if normalized_val == 0:
			normalized_val = 1
		dic[key]= normalized_val
	return dic

# writes the normalized dict in a txt to be pasted manually in wordle.net
def dict_to_txt_for_wordle(dict_in, filename, sort_key=lambda t:t, value_key=lambda t:t):
	if not dict_in:
		dict_in = {'No hashtags found':1}
	ordered_list = []
	dict_in = normalize_dict(dict_in)
	for key, value in dict_in.items():
		ordered_list.append([key, value_key(value)])	
	ordered_list = 	sorted(ordered_list, key=sort_key, reverse=True)	
	out = open(filename, 'w', encoding= 'utf-8')
	for item in ordered_list[:120]:		
		i = 0
		while i < item[1]:
			out.write(item[0] + ' ')
			i+=1	
	out.close()	

# creates a CSV file of the latitude and longitude data of the tweets
def locations_to_csv(dict_in, filename='locations.csv'):
	with open(filename, 'w', newline='', encoding="utf8") as csvfile:
		file_writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)	
		file_writer.writerow(['latitude', 'longitute'])
		for key, value in dict_in.items():
			file_writer.writerow([value[0], value[1]])
		csvfile.close()

# creates a CSV file of the dictionary data received
def top_something_to_csv(dict_in, filename, column_titles, reverse, sort_key, value_format=lambda t: t):
	ordered_list = []
	for key, value in dict_in.items():
		ordered_list.append([key, value_format(value)])
	ordered_list = sorted(ordered_list, key=sort_key, reverse=reverse)
	with open(filename, 'w', newline='', encoding="utf8") as csvfile:
		file_writer = csv.writer(csvfile, delimiter='|', quotechar='"', quoting=csv.QUOTE_MINIMAL)	
		file_writer.writerow(column_titles)
		for item in ordered_list:
			file_writer.writerow([item[0], item[1]])
		csvfile.close()

# returns error message with the corrupted line and exits the program
def error_parsing(line_num):
	print("Erro na linha: "+ str(line_num))	
	print("Erro: Nem todos tweets foram parseados. Encerrando...")
	sys.exit()

def initialize_file(filename, list_str_columns_titles):
	with open(filename, 'w', newline='', encoding='utf8') as csvfile:
		file_writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)	
		file_writer.writerow(list_str_columns_titles)
