#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    This module contains functions and constants used to clean and filter
    words in texts.
    Some third party modules can be used with this module, if you want to improve it
    * python-nltk for more stopwords;
    * rfc3987 to better identify URLS;
    * a lot of twitter third party API's to identify hashtags, URLS etc.

    The libraries above are not currently used to make the script easier to install 
    for end users.
"""
import string
from customized_stopwords import portuguese_common_words

""" 
This list is defined in it's own file in order to make modifications 
easier for non-programmers.
Check python ntlk for better stopwords in your language.
"""
CUSTOMIZED_STOPWORDS = set(portuguese_common_words)

VALID_CHARACTERS = string.ascii_letters + string.digits

ACCENT_REPLACEMENTS = {
    ord('á'):'a',
    ord('à'):'a',
    ord('è'):'e',
    ord('é'):'e',
    ord('í'):'i',
    ord('ì'):'i',
    ord('ò'):'o',
    ord('ó'):'o',
    ord('ù'):'u',
    ord('ú'):'u',
    ord('ü'):'u'
}

def remove_latin_accents(str_string):
    """ 
    This function replaces characters with accents 
    with non accented characters.
    """
    return str_string.translate(ACCENT_REPLACEMENTS)

def remove_invalid_characters(str_string):
    """
    Removes all characters from a string that aren't 
    letters or numbers. 
    """
    list_string_valid_chars = []
    for character in str_string:
        if character in VALID_CHARACTERS:
            list_string_valid_chars.append(character)
    if len(list_string_valid_chars) == 0:
        return None
    else:
        return ''.join(list_string_valid_chars)

def is_stopword(str_string):
    """ Returns True if str_string is the stopwords list or False if not. """
    if str_string in CUSTOMIZED_STOPWORDS:
        return True
    else:
        return False

def is_hashtag(str_s):
    """ 
    Returns True if the input is a hashtag or False if not.
    A hashtag is considered as string that starts with the "#"
    character.
    """
    if str_s.startswith("#"):
        return True
    else:
        return False

def is_twitter_mention(str_s):
    """ 
    Returns True if the input is a twitter mention and False if not.
    A twitter mention is considered a string that startws with the "@"
    character.
    """
    if str_s.startswith("@") or str_s.startswith("＠"):
        return True
    else:
        return False

def is_URL(str_s):
    """ 
    Returns True if str_string is an URL or False if not. """
    if str_s.startswith("ht") or str_s.startswith('hr'):
        return True
    else:
        return False

def is_valid_twitter_short_url(str_s):
    """ 
    Checks if a URL is a valid shortened twitter URL. 
    The shortened link length increases with time and can 
    be found on twitter API documentation, or obtained during 
    the execution of the script with ajax.
    #FIXME: get the short URL length dynamically from twitter.
    """
    if len(str_s) in [22,23]:
        return True
    else:
        return False