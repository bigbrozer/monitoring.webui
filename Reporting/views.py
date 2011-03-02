# Reporting app views

# Django imports
from django.shortcuts import render_to_response
from django.http import HttpResponse

# Models
from optools.Reporting.models import AckStat

# Open Flash Chart imports
import openFlashChart
from openFlashChart_varieties import (Bar, x_axis_labels)

# Utility
import math

# The view that show graph about status
def status(request):
	title = 'Status overview for active alerts'
	return render_to_response('reporting/status.html', {'title': title})

# Create graph data for status, return json data
def status_data(request):
	# Some var used in this view
	weeks = []
	warning_bar_values = []
	critical_bar_values = []
	y_max_limit = 10
	
	# Query DB to get values of last 5 entries
	for stat in AckStat.objects.order_by('-date')[0:5]:
		week = stat.date.isocalendar()[1]
		year = stat.date.isocalendar()[0]
		
		weeks.insert(0, 'Week {0!s} - {1!s}'.format(week, year))
		warning_bar_values.insert(0, stat.active_ack_warn)
		critical_bar_values.insert(0, stat.active_ack_crit)
	
	# Compute MAX value that could be in graph for Y axis limit
	if max(warning_bar_values) > max(critical_bar_values):
		y_max_limit = math.ceil(max(warning_bar_values) / 10.) * 10
	else:
		y_max_limit = math.ceil(max(critical_bar_values) / 10.) * 10
	
	# Graphs creation
	warning = Bar(text = 'Warning', values = warning_bar_values)
	warning.set_colour('#DDDD00')
	warning.set_tooltip(r'Warning<br>Value:#val#')
	critical = Bar(text = 'Critical', values = critical_bar_values)
	critical.set_colour('#FF0000')
	critical.set_tooltip(r'Critical<br>Value:#val#')

	chart = openFlashChart.template('Acknowledged Alerts')
	chart.add_element(warning)
	chart.add_element(critical)
	chart.set_x_axis(labels = x_axis_labels(labels = weeks))
	chart.set_y_axis(max = y_max_limit, steps = 5)
	chart.set_bg_colour('#FFFFFF')

	return HttpResponse(chart.encode())
