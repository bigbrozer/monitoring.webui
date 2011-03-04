# Reporting app views

# Django imports
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.template import RequestContext

# Models
from optools.Reporting.models import AckStat, ProcedureStat

# Open Flash Chart imports
import openFlashChart
from openFlashChart_varieties import (Bar, Pie, pie_value, x_axis_labels)

# Utility
import math

# The view that show graph about stats
def stats(request):
	title = 'Statistical overview for Nagios'
	return render_to_response('reporting/status.html', {'title': title}, context_instance=RequestContext(request))

# Create graph data for ack alerts, return json data
def ack_stat_data(request):
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
	warning.set_on_show(anim_type = 'pop', cascade = 1, delay = 0.5)
	
	critical = Bar(text = 'Critical', values = critical_bar_values)
	critical.set_colour('#FF0000')
	critical.set_tooltip(r'Critical<br>Value:#val#')
	critical.set_on_show(anim_type = 'fade-in', cascade = 1, delay = 0.3)

	chart = openFlashChart.template('Acknowledged Alerts')
	chart.add_element(warning)
	chart.add_element(critical)
	chart.set_x_axis(labels = x_axis_labels(labels = weeks))
	chart.set_y_axis(max = y_max_limit, steps = 5)
	chart.set_bg_colour('#FFFFFF')

	return HttpResponse(chart.encode())

# Create graph data for procedure stats, return json data
def procedure_stat_data(request):
	# Some var used in this view
	proc_stats = (
		pie_value(ProcedureStat.objects.order_by('-date')[0].num_with_procedure, label = ('With', None, None), colour = '#00EE00'),
		pie_value(ProcedureStat.objects.order_by('-date')[0].num_no_procedure, label = ('Without', None, None), colour = '#FF0000'),
	)
	
	# Graphs creation	
	procedure = Pie(values = proc_stats)

	chart = openFlashChart.template('Procedures statistics')
	chart.add_element(procedure)
	chart.set_bg_colour('#FFFFFF')

	return HttpResponse(chart.encode())

