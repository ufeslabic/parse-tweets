labic-parse-tweets
==================

------------------
Purpose:
------------------
This script was created to parse tweets collected by Your Twapper Keeper(https://github.com/540co/yourTwapperKeeper), an open source tool to archive tweets.
After the tweets are archived, you can dump then in some formats. This script specifically, works with pipe delimited csv's.

------------------
Requirements:
------------------
* Linux
* Python 3.3

------------------
Usage:
------------------
* Download the files
* Put the files and the tweets exported from your twapper keeper on the same folder
* Rename the file exported from ytk to "tweets.csv"
* call the script on a shell in this folder;

Example:
python3.3 parse_tweets.py

------------------
Results
------------------
When the script is done the results will be in the same folder. The files created are:

Some pipe delimited csv's:

* dates.csv:		number of tweets per day in the given dataset;

* hashtags.csv: 	number of users using the hashtags;

* urls.csv: 		urls with the number of distinct users that mentioned it

* locations.csv: 	geo coords of the tweets. The number is significantly smaller than the whole dataset because a very small number of tweets have geographical data.

* users_activity.csv: contains the number of tweets per user

* mentions.csv: most mentioned profiles

* words_per_period: table with a timeline of the top 10(default) words in a given dataset

Two txt's to be used with Wordle(http://www.wordle.net/create) or Tagxedo to generate and customize your wordclouds:

* top_words_wordle.txt: Text containing the most mentioned words of the tweets. Paste it on wordle.net to generate a wordcloud that you can customize.

* top_hashtags_wordle.txt: Text containing the most mentioned hashtags of the tweets. Paste it on wordle.net to generate a wordcloud that you can customize.





