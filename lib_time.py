#!/usr/bin/env python
# -*- coding: utf-8 -*-

from itertools import groupby
import datetime, csv

# returns the N topwords of a list
def get_N_first(words, number):
		aux = []
		top_words = []	
		for key, value in words.items():
			top_words.append([key, value])
		top_words.sort(key=lambda x:x[1], reverse=True)		
		for item in top_words:
			aux.append(item[0])
		return(aux[:number])

# function used as key for the group by to group by day
def time_period_grouper(start_date, some_date):
	return(some_date-start_date).days // 1


def word_over_time(timestamps_list):
	startdate = min(timestamps_list)	
	rounded_startdate = startdate.strftime('%d/%m/%Y')
	rounded_startdate = datetime.datetime.strptime(rounded_startdate, '%d/%m/%Y')
	timestamps_list.sort()
	word_per_day = {}
	for day, number_of_dates in groupby(timestamps_list, key=lambda x:time_period_grouper(rounded_startdate, x)):
		word_per_day[day] = len(list(number_of_dates))
	return word_per_day
		
def create_time_steps(timestamps_list):	
	time_step = min(timestamps_list)
	time_step = time_step.strftime('%d/%m/%Y')
	time_step = datetime.datetime.strptime(time_step, '%d/%m/%Y')
	delta = datetime.timedelta(1) #one day delta
	step_number = 0
	time_intervals = []
	while time_step < max(timestamps_list):
		time_intervals.append((time_step, step_number))
		time_step = time_step + delta
		step_number += 1
	return sorted(time_intervals, key= lambda x: x[1]) #[(datetime, day_number), ...]

def timeline(words_per_time, list_of_words, timestamps_list):
	grouped_by_words = {}
	if not(timestamps_list):
		print("Error generating timeline: not enough data. Specifying more profiles in the cluster_usernames.csv file may solve this.")
		return
	for word in list_of_words:
		try:
			grouped_by_words[word] = word_over_time(words_per_time[word])
		except KeyError:
			pass	
	with open('words_per_period.csv', 'w', newline='', encoding="utf8") as csvfile:
		file_writer = csv.writer(csvfile, delimiter='|', quotechar='"', quoting=csv.QUOTE_MINIMAL)
		file_writer.writerow(['*'] + list_of_words)
		for period in create_time_steps(timestamps_list):
			line = [datetime.datetime.strftime(period[0], '%d/%m/%y')]
			for word in list_of_words:
				try:
					value = grouped_by_words[word][period[1]]
				except:
					value = 0
				line.append(value)
			file_writer.writerow(line)