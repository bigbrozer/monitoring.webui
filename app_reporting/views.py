# Reporting app views

# Django imports
from django.shortcuts import render_to_response
from django.http import HttpResponse

# Open Flash Chart imports
import openFlashChart
from openFlashChart_varieties import (Bar, x_axis_labels)

from datetime import datetime

# The view that show graph about status
def status(request):
	title = 'Status overview for active alerts'
	return render_to_response('reporting/status.html', {'title': title})

# Create graph data for status, return json data
def status_data(request):
	# Date calculation
	now = datetime.now()
	current_year = now.year
	current_week = now.isocalendar()[1]
	weeks = []
	for i in range(5):
		if current_week == 1:
			current_week = 53
			current_year -= 1
		current_week -= 1
		weeks.insert(0, 'Week {0!s} - {1!s}'.format(current_week, current_year))
	
	# Graphs creation
	warning = Bar(text = 'Warning', values = range(6, 1, -1))
	warning.set_colour('#DDDD00')
	warning.set_tooltip(r'Warning<br>Value:#val#')
	critical = Bar(text = 'Critical', values = range(1, 6, 1))
	critical.set_colour('#FF0000')
	critical.set_tooltip(r'Critical<br>Value:#val#')

	chart = openFlashChart.template('Acknowledged Alerts')
	chart.add_element(warning)
	chart.add_element(critical)
	chart.set_x_axis(labels = x_axis_labels(labels = weeks))

	return HttpResponse(chart.encode())
