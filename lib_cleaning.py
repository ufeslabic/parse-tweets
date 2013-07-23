#!/usr/bin/env python
# -*- coding: utf-8 -*-
import string
from customized_stopwords import portuguese_common_words

# check python ntlk for better stopwords in your language
stopwords = set(portuguese_common_words)

# characters to be excluded from strings
weird_characters = set(string.punctuation)
weird_characters.add('”') # curly opening quote 
weird_characters.add('“') # curly closing closing quote
weird_characters.add('‘')
weird_characters.add('…')

# remove punctuaction signs
def remove_punctuaction(word):	
	hashtag = ''.join(character for character in word if character not in weird_characters)
	hashtag = hashtag.replace(" ","")	
	return hashtag.replace('”','')

