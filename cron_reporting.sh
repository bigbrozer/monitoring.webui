#!/bin/bash

source ~/Envs/stage/bin/activate

cd $HOME/reporting

./get_fresh_redmine.sh
./get_kb_pages.sh
python ./jobs/insert.py

