#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    This module contains functions and constants used to clean and filter
    words in texts.
"""
import string
from customized_stopwords import portuguese_common_words

""" 
This list is defined in an isolated file in order to make modifications 
easier for non-programmers.
"""
CUSTOMIZED_STOPWORDS = set(portuguese_common_words) # check python ntlk for better stopwords in your language

""" 
Characters to be excluded from the strings. Some characters not covered 
by Python's string.punctuation were added as needed.
"""
UNDESIRED_CHARACTERS = set(string.punctuation)
UNDESIRED_CHARACTERS.add('”')
UNDESIRED_CHARACTERS.add('“')
UNDESIRED_CHARACTERS.add('‘')
UNDESIRED_CHARACTERS.add('…')

def remove_punctuation(str_string):
    """ 
    This function iterates through each character in 'str_string'
    and concatenate them in a new string if it is not in the 
    'UNDESIRED_CHARACTERS' set. It returns the given string without 
    the UNDESIRED_CHARACTERS, even if it is the empty string.
    """
    str_clean_string = ''.join(character for character in str_string if character not in UNDESIRED_CHARACTERS)
    if str_clean_string == '':
        return None
    else:
        return str_clean_string
