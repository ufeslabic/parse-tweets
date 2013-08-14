#!/bin/sh
sed 's/\x0/ /g' tweets.csv > tweets_FIXED.csv
