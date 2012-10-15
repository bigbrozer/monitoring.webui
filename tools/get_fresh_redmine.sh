#!/bin/bash

PROGPATH=$(dirname $0)

scp monitoring-dc.app.corp:/var/lib/dbconfig-common/sqlite3/redmine/instances/default/redmine_default "${PROGPATH}/../var/."
