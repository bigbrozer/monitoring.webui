#!/bin/bash

source ~/Envs/stage/bin/activate

cd $HOME

./get_fresh_redmine.sh
python ./reporting/jobs/insert.py

