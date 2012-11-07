#!/bin/bash

PROGPATH=$(dirname $0)

rsync -avz --delete monitoring-dc.app.corp:/var/www/kb/data/pages "${PROGPATH}/../var"
rsync -avz --delete monitoring-dc.app.corp:/var/www/kb/data/meta "${PROGPATH}/../var"
