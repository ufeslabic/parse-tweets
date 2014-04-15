#!/usr/bin/env python
# -*- coding: utf-8 -*-
import csv

GEPHI_DELIMITER =';'
DEFAULT_INPUT_DELIMITER = '|'
INPUT_FILE ='tweets_FIXED_NO_DUPLICATES.csv'

def tweets_to_csv(list_csv_lines, filename='tweets_with_geocoordinates.csv'):
    with open(filename, 'w', newline='', encoding="utf8") as csvfile:       
        file_writer = csv.writer(csvfile, delimiter=GEPHI_DELIMITER, quoting=csv.QUOTE_MINIMAL)
        for line in list_csv_lines:
            file_writer.writerow(line)
        csvfile.close()

if __name__ == '__main__':
    lis_lines_to_write = []
    with open(INPUT_FILE, 'rt', encoding="utf8") as csvfile:
        try:
            csv_in = csv.reader(csvfile, delimiter=DEFAULT_INPUT_DELIMITER, quoting=csv.QUOTE_MINIMAL)
            lis_lines_to_write.append(next(csv_in)) #saves the line with the column titles.
            
            try:
                for line in csv_in:
                    if (len(line) is 13) and (line[8] == 'Point'):
                        lis_lines_to_write.append(line)
            except (UnicodeDecodeError, IndexError):
                print(line)
                error_parsing(csv_in.line_num)            
            
            tweets_to_csv(lis_lines_to_write, 'tweets_with_geocoordinates.csv')
        except (IOError, StopIteration):
            print("Error opening some necessary files.")
            print("Make sure you have a 'tweets_FIXED_NO_DUPLICATES.csv' file in this folder.")
            print("Please ensure that you are not running the script as root.")



