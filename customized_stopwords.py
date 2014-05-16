#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" 
This module contains a constantly changing list of stopwords 
to be used by the script. Feel free to add more words relevant 
to your needs(or dataset). 

You can also use python-nltk to get some stopwords for your language.
"""

portuguese_common_words = ['a', 
'acha', 'acho', 'ae', 'aeh', 'ah', 'ai', 'aih', 'aih', 'ainda', 
'algo', 'ao', 'aos', 'após', 'aquela', 'aquele', 'aqui', 'as', 
'ateh', 'até', 'aug', 'axovc', 'aé', 'aê', 'aí', 'aí', 
'cada', 'com', 'contudo', 'cuja', 'cujo', 'cê', 
'da', 'da', 'dah', 'daki', 'daqi', 'daqui', 'das', 'de', 
'de', 'dela', 'dela', 'dele', 'delepara', 'dessa', 'desse', 
'desta', 'deste', 'devemos', 'disso', 'diz', 'do', 
'dos', 'dum', 'duma', 'durante', 'dá', 'eh', 'eh', 'ei', 
'ela', 'ela', 'elaslhe', 'ele', 'ele', 'ele', 'eles', 
'em', 'em', 'enfim', 'entao', 'entaum', 'entaun', 'entretanto', 
'então', 'era', 'essa', 'esse', 'esta', 'esta', 'estah', 'estao', 
'estar', 'este', 'está', 'estão', 'eu', 'fala', 'faz', 'fazer', 
'foi', 'for', 'fosse', 'ha', 'ha ha ha', 'he he he', 'hi hi hi', 
'ho ho ho', 'hora', 'há', 'ia', 'ir', 'iria', 'irá', 'isso', 'isto', 
'iá', 'ja', 'jah', 'já', 'já', 'la', 'lah', 'lhe', 'lá', 'lá', 
'mais', 'manda', 'mas', 'me', 'mesmo', 'meu', 'mim', 'minha', 
'mt', 'mto', 'mtu', 'na', 'nao', 'nas', 'naum', 'neh', 'nesta', 'no', 
'noix', 'nos', 'nova', 'num', 'não', 'né', 'nóis', 'nós', 'o', 'oi', 
'onde', 'os', 'ou', 'para', 'para', 'pela', 'pelo', 'pois', 'por', 
'por', 'portanto', 'pq', 'pra', 'pra', 'pro', 'pôr', 'qt', 'quanto', 
'que', 'que', 'quê', 'relnofollowfacebooka', 'relnofollowtwitter', 
'rt', 'rt', 'se', 'se', 'sem', 'ser', 'seu', 'seu', 'sim', 'sim', 
'so', 'sobre', 'sobreser', 'soh', 'soh', 'somos', 'sua', 'sua', 
'só', 'só', 'ta', 'tabem', 'taben', 'tah', 'tal', 'tambem', 
'também', 'tamem', 'tamen', 'tanta', 'tanto', 'tava', 'tb', 
'tbm', 'tchau', 'te', 'tem', 'tem', 'ter', 'terde', 'teu', 
'teve', 'to', 'todavia', 'todo', 'tomem', 'tu', 'tua', 'tá', 
'tô', 'tô', 'um', 'uma', 'umas', 'uns', 'vai', 'vamo', 'vamos', 'como'
'vc', 'vcs', 'veio', 'vez', 'via', 'vier', 'vim', 'vin', 
'vir', 'voces', 'vocês', 'vou', 'vão', 'às', 'ás', 'como']

spanish_common_words = ['de', 'la', 'que', 'el', 'en', 'y', 'a', 'los', 'del', 'se', 'las', 'por', 'un', 
'para', 'con', 'no', 'una', 'su', 'al', 'lo', 'como']

english_common_words = ["tis","'twas","a","able","about","across","after",
"ain't","all","almost","also","am","among","an","and","any","are","aren't","as",
"at","be","because","been","but","by","can","can't","cannot","could","could've","couldn't",
"dear","did","didn't","do","does","doesn't","don't","either","else","ever","every","for",
"from","get","got","had","has","hasn't","have","he","he'd","he'll","he's","her","hers","him",
"his","how","how'd","how'll","how's","however","i","i'd","i'll","i'm","i've","if","in","into",
"is","isn't","it","it's","its","just","least","let","like","likely","may","me","might","might've",
"mightn't","most","must","must've","mustn't","my","neither","no","nor","not","of","off","often","on",
"only","or","other","our","own","rather","said","say","says","shan't","she","she'd","she'll","she's",
"should","should've","shouldn't","since","so","some","than","that","that'll","that's","the","their","them",
"then","there","there's","these","they","they'd","they'll","they're","they've","this","tis","to","too","twas",
"us","wants","was","wasn't","we","we'd","we'll","we're","were","weren't","what","what'd","what's","when","when",
"when'd","when'll","when's","where","where'd","where'll","where's","which","while","who","who'd","who'll","who's",
"whom","why","why'd","why'll","why's","will","with","won't","would","would've","wouldn't","yet","you","you'd","you'll",
"you're","you've","your", "cant", "ive", "dont", "want", "follow", "thisit", "year", "rt", "im", "doesnt", "away", "here",
"reuters", "mine", "many", "de", "still", "next", "know", "until", "video", "till", "yours", "indian", "india", "pakistan",
"sochi", "gt", "amp", "cricket", "ha", "da", "del","el","fa","fi", "hai","hes","hey","hi","id","icc","ind","ka",
"ke","ki","ko","la","lol","loc","mt","mls","mat","ne","odi","nz","odi","oh","ok","ovr","pak","php","rugby","sa","se","sl","snd",
"sri","til","van","via","wi","wkt","whos","without","wont","whos","whats","went","wow","youare","yes","ya"]