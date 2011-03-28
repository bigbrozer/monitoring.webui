#!/usr/bin/env python
#-*- coding:utf-8 -*-

import sys, os

# Adding optools project to sys.path
optools_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(optools_dir)
os.environ['DJANGO_SETTINGS_MODULE'] = 'optools.settings'

from optools.apps.downtime.commands import ScheduleFullDowntime

command = ScheduleFullDowntime('NAGIOS_DC_SATELLITE_AVS', '03/28/2012 19:00', '03/29/2012 00:00', '0besancon', 'Maintenance')
command.send()

