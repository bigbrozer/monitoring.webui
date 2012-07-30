#!/bin/bash

PROGPATH=$(dirname $0)

source $HOME/Envs/stage/bin/activate

cd "$PROGPATH"

./get_fresh_redmine.sh
./get_kb_pages.sh
python ./jobs/insert.py

