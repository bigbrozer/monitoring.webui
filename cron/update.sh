#!/bin/bash

PROGPATH=$(dirname $0)
source $HOME/Envs/optools/bin/activate
python $PROGPATH/../jobs/insert.py 2>&1 >/tmp/reporting.log
