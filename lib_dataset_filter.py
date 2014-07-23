#!/usr/bin/env python
# -*- coding: utf-8 -*-
import csv
import os
import sys
from lib_input import DEFAULT_INPUT_DELIMITER
from lib_output import DEFAULT_OUTPUT_DELIMITER
from lib_input import load_filter_list

def is_username_in_tweet_text(str_username, str_tweet_text):
    return(str_username in str_tweet_text)

def filter_dataset(str_input_filename, set_media_usernames):
    print("Filtering dataset with the profiles specified in mídia.csv")
    set_tuple_filtered_lines = set()
    set_tuple_all_lines = set()
    for str_username in set_media_usernames:        
        with open(str_input_filename, 'rt', encoding="utf8") as csvfile:            
            csv_in = csv.reader(csvfile, delimiter=DEFAULT_INPUT_DELIMITER, quoting=csv.QUOTE_NONE)
            # Save the first line, because sets aren't ordered.
            list_str_first_line = next(csv_in)

            # Adding all the lines in the set.
            for line in csv_in:
                set_tuple_all_lines.add(tuple(line))
                temp_username = line[2].lower()                
                #if the username is in the media usernames list
                if(temp_username in set_media_usernames):
                    set_tuple_filtered_lines.add(tuple(line))
                else:                    
                    str_tweet_text = line[0].lower()
                    #if the username is NOT in the media usernames list, check if it occurs in the tweet text
                    if(is_username_in_tweet_text(str_username, str_tweet_text)):
                        set_tuple_filtered_lines.add(tuple(line))                
    
    # Writing all the exclusive lines
    with open("tweets_filtered_media.csv", 'w', newline='', encoding="utf8") as csvfile:
        file_writer = csv.writer(csvfile, delimiter=DEFAULT_OUTPUT_DELIMITER, quotechar='"')
        file_writer.writerow(list_str_first_line)
        for line in set_tuple_filtered_lines:
            file_writer.writerow(line)

    with open("tweets_filtered_no_media.csv", 'w', newline='', encoding="utf8") as csvfile:
        file_writer = csv.writer(csvfile, delimiter=DEFAULT_OUTPUT_DELIMITER, quotechar='"')
        file_writer.writerow(list_str_first_line)
        set_tuple_lines_without_media = set_tuple_all_lines - set_tuple_filtered_lines
        for line in set_tuple_lines_without_media:
            file_writer.writerow(line)

    print("tweets_filtered.csv File was created.")

def filter_tweets_without_RT(str_input_filename):
    set_tuple_filtered_lines = set()
    with open(str_input_filename, 'rt', encoding="utf8") as csvfile:
        csv_in = csv.reader(csvfile, delimiter=DEFAULT_INPUT_DELIMITER, quoting=csv.QUOTE_NONE)
        # Save the first line, because sets aren't ordered.
        list_str_first_line = next(csv_in) 

        # Adding all the lines in the set.
        for line in csv_in:
            str_tweet_text = line[0].lower()
            if("rt @" not in str_tweet_text):                
                set_tuple_filtered_lines.add(tuple(line))                
    
    # Writing all the exclusive lines
    with open("tweets_without_RTs.csv", 'w', newline='', encoding="utf8") as csvfile:
        file_writer = csv.writer(csvfile, delimiter=DEFAULT_OUTPUT_DELIMITER, quotechar='"')
        file_writer.writerow(list_str_first_line)
        for line in set_tuple_filtered_lines:
            file_writer.writerow(line)
    print("tweets_without_RTs.csv File was created.")

def file_filter():
    """ This function removes null_byte and duplicate tweets. """
    str_file_with_screenames_to_filter = 'mídia.csv'
    set_media_usernames = set(load_filter_list(str_file_with_screenames_to_filter))
    filter_tweets_without_RT('tweets_FIXED.csv')
    if (not set_media_usernames):
        return
    else:
        filter_dataset('tweets_FIXED.csv', set_media_usernames)
    




