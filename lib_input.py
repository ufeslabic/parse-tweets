#!/usr/bin/python
# coding: utf-8
import sys, subprocess, getopt

# parses the command line options
def options_parser(argv):
	arguments = {}
	try:
		opts, args = getopt.getopt(argv[1:], 'w:h:', ['hashtags=', 'words='])
	except getopt.GetoptError:
		print("Parâmetros inválidos")
		sys.exit(2)
	for opt, arg in opts:
		if opt in ('-h', '--hashtags'):
			pass					
		elif opt in ('-w', '--words'):
			arguments['number_of_words'] = int(arg)
	if('number_of_words' not in arguments):
		arguments['number_of_words'] = 10 # setting default number of words	
	if('hashtags' not in arguments):
		arguments['number_of_hashtags'] = 10 # setting default number of hashtags	
	return(arguments)

# calls a bash script to rewrite the tweets.csv file renaming it as tweets_FIXED.csv without the null byte character
# tweets_FIXED.csv is the file is that will be used by the script
def remove_null_byte():
	subprocess.call(["sh", "remove_null_byte.sh"])
