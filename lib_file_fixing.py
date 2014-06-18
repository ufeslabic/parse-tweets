#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" 
This module contains functions to remove duplicate lines from CSV files and
remove the null byte character. It lazily reads all the file at once, so you may 
need a lot of memorym depending on the size of your CSV.
"""

import csv
import os
import sys
from lib_input import DEFAULT_INPUT_DELIMITER
from lib_output import DEFAULT_OUTPUT_DELIMITER

def filename_append(str_filename, str_text_to_append):
    """ This function appends a string to the end of a given filename """
    str_filename, str_file_extension = os.path.splitext(str_filename)
    new_filename = str_filename + str_text_to_append + str_file_extension
    return new_filename

def remove_null_byte(str_input_filename='tweets.csv'):
    # rb: the B is for byte
    file_input = open(str_input_filename,"rb")

    # Read the whole CSV at once.
    str_whole_csv = file_input.read()
    file_input.close()

    # Replace the null byte with the empty string.
    str_whole_csv = str_whole_csv.replace(b'\x00', bytes('', 'utf-8'))

    # Writes the resulting file
    str_fixed_filename = filename_append(str_input_filename, '_FIXED')
    file_output = open(str_fixed_filename, 'wb')
    file_output.write(str_whole_csv)
    file_output.close()

def remove_duplicate_lines(str_input_filename='tweets_FIXED.csv'):
    """ 
    This function removes all duplicate lines in a given CSV.
    A line is considered duplicate if another one with the exact 
    same column values exist.
    """

    # Empty set to store all the lines. Sets doesn't keep two copies of the 
    # same object duplicate objects. If an already existing object is trying 
    # to be inserted nothing will happen.
    set_tuple_valid_lines = set()
    int_total_lines = 0
    int_total_valid_lines = 1 #to account for the headers
    with open(str_input_filename, 'rt', encoding="utf8") as csvfile:
        csv_in = csv.reader(csvfile, delimiter=DEFAULT_INPUT_DELIMITER, quoting=csv.QUOTE_NONE)
        # Saving the first line, because sets aren't ordered.
        list_str_first_line = next(csv_in) 

        # Adding all the lines in the set.
        for line in csv_in:
            if len(line) is 13:
                int_total_valid_lines += 1                
                set_tuple_valid_lines.add(tuple(line))
    int_total_lines = csv_in.line_num
    int_total_valid_lines_non_duplicate = len(set_tuple_valid_lines) + 1 #to account for the column titles
    str_fixed_filename = filename_append(str_input_filename, '_NO_DUPLICATES')
    
    print(str(int_total_valid_lines) + "\t lines before cleaning.")
    print(str(int_total_valid_lines - int_total_valid_lines_non_duplicate) + "\t duplicate lines.")
    
    # Writing all the exclusive lines
    with open(str_fixed_filename, 'w', newline='', encoding="utf8") as csvfile:
        file_writer = csv.writer(csvfile, delimiter=DEFAULT_OUTPUT_DELIMITER, quotechar='"')
        file_writer.writerow(list_str_first_line)
        for line in set_tuple_valid_lines:
            line2 = list(line)
            line2 = line2[0].replace("\n", " ").replace("\r","").replace("|","")            
            file_writer.writerow(line)    

def file_fix(str_input_filename):
    """ This function removes null_byte and duplicate tweets. """
    remove_null_byte(str_input_filename)
    str_temp_filename = filename_append(str_input_filename, '_FIXED')
    remove_duplicate_lines(str_temp_filename)

if __name__ == '__main__':
    str_input_filename = sys.argv[1]
    file_fix(str_input_filename)



