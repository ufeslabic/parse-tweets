#!/usr/bin/python
# coding: utf-8
import os, sys, csv

# Removes null byte from file, but currently not being used. 
# It was replaced by the command
# sed 's/\x0/ /g' tweets.csv > tweets_FIXED.csv
# Only used to find unicode errors on the csv
def remove_null_byte(filename, delimiter):
	sys.stderr.write('Uma cópia do arquivo "tweets.csv" chamada "tweets_FIXED.csv" foi criada...\n')
	corrupted_lines = []
	total_errors = 0
	with open(filename[:-4] + '_FIXED.csv', 'w', encoding="utf8") as csv_out:
		file_writer = csv.writer(csv_out, delimiter=delimiter, quotechar='"', quoting=csv.QUOTE_MINIMAL)
		with open(filename, 'rt', encoding="utf8") as csv_in:
			csvfile = csv.reader(csv_in, delimiter=delimiter, quotechar='"')
			try:				
				for line in csvfile:									
					file_writer.writerow(line[:-1]+[line[-1].replace(";","")])				
			except UnicodeDecodeError as e:
				corrupted_lines.append(csvfile.line_num)
				print("Erro de Unicode na linha: "+ str(csvfile.line_num))				
			except csv.Error as e:
				corrupted_lines.append(csvfile.line_num)
				print("Erro de null byte na linha: "+ str(csvfile.line_num))
