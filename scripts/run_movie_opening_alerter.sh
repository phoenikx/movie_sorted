#!/usr/bin/env bash
DATE=`date +%Y_%m_%d`;
source $HOME/.virtualenvs/projects/movie_sorted/bin/activate && cd $HOME/projects/movie_sorted && . export_envs.sh && python3 movie_opening_alerter/movie_opening_alerter.py $1 $2 $3 $4 $5 >> ../logs/movie_opening_alerter/$DATE-$2.log

