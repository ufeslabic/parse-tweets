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
from customized_stopwords import portuguese_common_words, english_common_words, spanish_common_words

""" 
This list is defined in it's own file in order to make modifications 
easier for non-programmers.
Check python ntlk for better stopwords in your language.
"""
CUSTOMIZED_STOPWORDS = set(portuguese_common_words+ spanish_common_words + english_common_words)

VALID_CHARACTERS = string.ascii_letters + string.digits
EXTRA_CHARACTERS = "_-"
VALID_CHARACTERS = VALID_CHARACTERS + EXTRA_CHARACTERS

VALID_CHARACTERS_SET = set([])

for character in VALID_CHARACTERS:
    VALID_CHARACTERS_SET.add(character)

ACCENT_REPLACEMENTS = {
    ord('á'):'a',
    ord('ã'):'a',
    ord('â'):'a',
    ord('à'):'a',
    ord('è'):'e',
    ord('ê'):'e',
    ord('é'):'e',
    ord('í'):'i',
    ord('ì'):'i',
    ord('ò'):'o',
    ord('ó'):'o',
    ord('ô'):'o',
    ord('õ'):'o',
    ord('ù'):'u',
    ord('ú'):'u',
    ord('ü'):'u',
    ord('ç'):'c'
}

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
        return ''
    else:
        return str_clean_string

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
        if character in VALID_CHARACTERS_SET:
            list_string_valid_chars.append(character)
    if len(list_string_valid_chars) == 0:
        return ''
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
    if str_s.startswith("#") and not(str_s.endswith("…")):
        return True
    else:
        return False

def is_twitter_mention(str_s):
    """ 
    Returns True if the input is a twitter mention and False if not.
    A twitter mention is considered a string that startws with the "@"
    character.
    """
    if (str_s.startswith("@") or str_s.startswith("＠")) and not(str_s.endswith("…")) :
        return True
    else:
        return False

def is_URL(str_s):
    """ 
    Returns True if str_string is an URL or False if not. """
    if (str_s.startswith("ht") or str_s.startswith('hr')) and not(str_s.endswith("…")):
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

def has_links(str):
    for word in str.split():
        if word.startswith("ht") or word.startswith('hr'):
            return True
    return False

def is_the_only_hashtag_in_text(str_hashtag, str_text_to_search):
    lis_str_hashtags = []
    str_words_in_tweet = str_text_to_search.split()
    for str_word in str_words_in_tweet:
        if str_word.startswith("#"):
            lis_str_hashtags.append(str_word)
    if (len(lis_str_hashtags) == 1) and (str_hashtag in lis_str_hashtags):
        return True
    else:
        return False

