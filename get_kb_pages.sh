#!/bin/bash

rsync -avz --delete monitoring-dc.app.corp:/var/www/kb/data/pages $HOME
