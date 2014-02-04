#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This module contains functions used in identify 
some relevant entities in a tweet.
"""

def is_hashtag(str_s):
    """ Returns True if the input is a hashtag and False if not."""
    if str_s.startswith("#"):
        return True
    else:
        return False

def is_mention(str_s):
    """ Returns True if the input is a mention and False if not."""
    if str_s.startswith("@"):
        return True
    else:
        return False

def is_valid_twitter_short_url(str_s):
    """ 
    Checks if a URL is a valid shortened twitter URL. 
    The shortened link length increases with time and can 
    be found on twitter API documentation, or obtained during 
    the execution of the script with ajax.
    #FIXME: get the URL length from twitter documentation.
    """
    if len(str_s) in [22,23]:
        return True
    else:
        return False
