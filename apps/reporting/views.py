# Reporting app views

# Django imports
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.template import RequestContext

# Models
from optools.apps.reporting.models import NagiosKPI

# Open Flash Chart imports
import openFlashChart
from openFlashChart_varieties import (Bar, Pie, pie_value, x_axis_labels)

# Reports imports
from optools.apps.reporting.reports.top import get_top_ack_alerts

# Utility
import math

# The view that show graph about stats
def stats(request):
	template_context = {
		'title': 'Statistical overview for Nagios',
	}
	
	try:
		top_ack_alerts = get_top_ack_alerts()
		template_context['top_ack_alerts'] = top_ack_alerts
	except Exception as e:
		top_ack_alerts_error = str(e)
		template_context['top_ack_alerts_error'] = top_ack_alerts_error
	
	return render_to_response('reporting/status.html', template_context, context_instance=RequestContext(request))

# Create graph data for ack alerts, return json data
def ack_stat_data(request):
	# Tests if we have value in DB
	if not NagiosKPI.objects.all():
		return HttpResponse('There is no data in database.')
	
	# Some var used in this view
	weeks = []
	warning_bar_values = []
	critical_bar_values = []
	y_max_limit = 10
	
	# Query DB to get values of last 5 kpis
	for stat in NagiosKPI.objects.order_by('-date')[0:5]:
		week = stat.date.isocalendar()[1]
		year = stat.date.isocalendar()[0]
		
		weeks.insert(0, 'Week {0!s} - {1!s}'.format(week, year))
		warning_bar_values.insert(0, stat.alert_ack_warn_total)
		critical_bar_values.insert(0, stat.alert_ack_crit_total)
	
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
	# Tests if we have value in DB
	if not NagiosKPI.objects.all():
		return HttpResponse('There is no data in database.')
	
	# Service stats
	svc_with_procedure = NagiosKPI.objects.order_by('-date')[0].service_with_kb
	svc_without_procedure = NagiosKPI.objects.order_by('-date')[0].service_without_kb
	
	# Compare with previous week
	try:
		svc_with_procedure_week_before = NagiosKPI.objects.order_by('-date')[1].service_with_kb
		svc_without_procedure_week_before = NagiosKPI.objects.order_by('-date')[1].service_without_kb
		svc_with_trends = svc_with_procedure - svc_with_procedure_week_before
		svc_without_trends = svc_without_procedure - svc_without_procedure_week_before
		
		label_with = 'With\n({0:+d})'.format(svc_with_trends)
		label_without = 'Without\n({0:+d})'.format(svc_without_trends)
	except IndexError:
		# No previous week in DB to calculate trends
		label_with = 'With'
		label_without = 'Without'
	
	# Pie chart values
	proc_stats = (
		pie_value(svc_with_procedure, label = (label_with, None, None), colour = '#00EE00'),
		pie_value(svc_without_procedure, label = (label_without, None, None), colour = '#FF0000'),
	)
	
	# Graphs creation	
	procedure = Pie(values = proc_stats)
	procedure.set_on_click(request.build_absolute_uri('/~django/reports/services_without_procedure_in_nagios.csv'))

	chart = openFlashChart.template('Procedures statistics\n(Click to download report)')
	chart.add_element(procedure)
	chart.set_bg_colour('#FFFFFF')

	return HttpResponse(chart.encode())

