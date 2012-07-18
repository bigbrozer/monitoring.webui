#!/bin/bash

source ~/Envs/stage/bin/activate

cd $HOME/reporting

./get_fresh_redmine.sh
python ./jobs/insert.py

