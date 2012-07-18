#!/bin/bash

source /usr/local/bin/virtualenvwrapper.sh

workon stage
cd ~/reporting/
python ./manage.py runserver monadm.edc.eu.corp:8080

