#!/bin/bash

PROGPATH=$(dirname $0)

source $HOME/Envs/stage/bin/activate

cd "$PROGPATH"
python ./manage.py runserver 0.0.0.0:8080

