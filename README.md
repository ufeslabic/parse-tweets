labic-parse-tweets
==================

------------------
Purpose:
------------------
This script was created to parse tweets collected by Your Twapper Keeper(https://github.com/540co/yourTwapperKeeper), an open source tool to archive tweets.
After the tweets are archived, you can dump then in some formats. This script works specifically with pipe delimited csv's as input.

------------------
Requirements:
------------------
* Python 3.3+

------------------
Usage:
------------------
* Download the files
* Put the files and the tweets exported from your twapper keeper on the same folder
* Rename the file exported from ytk to "tweets.csv"
* If you want to run considering only a specific set of twitter usernames create a file named 'cluster_usernames.csv' in the same folder that your 'tweets.csv' file is. One username per line, like in the 'cluster_usernames_EXAMPLE.csv' file.
* NEW: If you want to run considering only tweets that have only one hashtag that you specify create a file named 'specific_hashtags.csv' in the same folder that your 'tweets.csv' file is, where the hashtag(with the '#'' character) is the only line in this file.
* If you want the script to run normally, just don't create a 'cluster_usernames.csv' file :)
* Call the script on a shell in this folder with the command below:

python3.3 parse_tweets.py

------------------
Results
------------------
When the script is done running the results will be in the 'RESULTS'. The files created are:

Some pipe delimited csv's:

* dates.csv:        number of tweets per day in the given dataset;

* hashtags.csv:     number of users using the hashtags;

* hashtags_without_accents.csv:  same as hashtags.csv except that all accents are removed;

* locations.csv:    geo coordinates of the tweets. The number is significantly smaller than the whole dataset because a very small number of tweets(less than 5%) have geographical data.

* mentions.csv: most mentioned profiles

* top_tweets.csv: top tweets ordered by number of RT's

* top_urls.csv: urls with the number of distinct users that mentioned it

* top_words.csv: file with the most 1000 mentioned words;

* tweets_with_links.csv: CSV file similar to the input tweets.csv, but only has the tweets from "tweets.csv" where the text has links;

* users_activity.csv: contains the number of tweets per user

* users_by_date.csv: contains the number of users per day

* words_per_period: table with a timeline of the top 10(default) words in a given dataset

One comma delimited CSV:

* hashtags_network.csv:     a csv file to be used with Gephi in order to generate a graph of hashtags;

And two txt files to be used with Wordle(http://www.wordle.net/create) or Tagxedo to generate and customize your wordclouds:

* top_words_wordle.txt: Text containing the most mentioned words of the tweets. Paste it on wordle.net to generate a wordcloud that you can customize.

* top_hashtags_wordle.txt: Text containing the most mentioned hashtags of the tweets. Paste it on wordle.net to generate a wordcloud that you can customize.

* top_hashtags_without_accents_wordle.txt: Same as top_hashtags_wordle, except that all accents are removed.


------------------
BETA
------------------
This script is in Beta stage, which means it may contain errors or inaccurate results. Feel free(and please do so!) to report any bugs you find. 

