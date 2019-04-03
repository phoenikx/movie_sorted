#!/usr/bin/env bash
echo "movie_name: $1"
echo "location: $2"
echo "movie_id: $3"
echo "emails: $4"
echo "movie_dates: $5"
DATE=`date +%Y_%m_%d`;
source $HOME/.virtualenvs/projects/movie_sorted/bin/activate && cd $HOME/projects/movie_sorted && . export_envs.sh && python3 movie_opening_alerter/movie_opening_alerter.py $1 $2 $3 $4 $5 >> ../logs/movie_opening_alerter/$DATE-$2.log

