#!/bin/sh
rm tweets_FIXED.csv
rm -f *.pyc
mkdir -p RESULTS
mv urls.csv RESULTS
mv dates.csv RESULTS
mv mentions.csv RESULTS
mv hashtags.csv RESULTS
mv locations.csv RESULTS
mv top_tweets.csv RESULTS
mv users_by_date.csv RESULTS
mv users_activity.csv RESULTS
mv hashtags_network.csv RESULTS
mv words_per_period.csv RESULTS 2> /dev/null
mv top_words_wordle.txt RESULTS
mv top_hashtags_wordle.txt RESULTS



