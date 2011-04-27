# Reporting app views

# Django imports
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.template import RequestContext
from django.db.models import Avg

# Models
from optools.apps.reporting.models import NagiosKPI

# Open Flash Chart imports
import openFlashChart
from openFlashChart_varieties import (Line, Bar_Stack, bar_stack_value, Pie, pie_value, x_axis_labels)

# Reports imports
from optools.apps.reporting.reports.top import get_top_ack_alerts

# Utility
import math
from datetime import date

# The view that show graph about stats
def stats(request):
	template_context = {
		'title': 'Nagios KPI',
	}
	
	try:
		top_ack_alerts = get_top_ack_alerts()
		template_context['top_ack_alerts'] = top_ack_alerts
	except Exception as e:
		top_ack_alerts_error = str(e)
		template_context['top_ack_alerts_error'] = top_ack_alerts_error
	
	return render_to_response('reporting/status.html', template_context, context_instance=RequestContext(request))

# Create graph data for alerts stats, return json data
def alerts_stat_data(request):
	# Tests if we have value in DB
	if not NagiosKPI.objects.all():
		return HttpResponse('There is no data in database.')
	
	# Some var used in this view
	weeks = []
	y_max_limit = 10
	
	# Bar stack graphs options
	stack_warn = Bar_Stack()
	stack_warn.append_keys(colour = '#9e9e00', text = 'Current Warning alerts', fontsize = 12)
	stack_warn.append_keys(colour = '#ffbf00', text = 'Detected Warning alerts', fontsize = 12)
	stack_warn.append_keys(colour = '#ffff00', text = 'Missed Warning alerts', fontsize = 12)
	stack_warn.set_tooltip('Warning: #val#<br>Total #total#')
	
	stack_crit = Bar_Stack()
	stack_crit.append_keys(colour = '#ff3f00', text = 'Current Critical alerts', fontsize = 12)
	stack_crit.append_keys(colour = '#760000', text = 'Detected Critical alerts', fontsize = 12)
	stack_crit.append_keys(colour = '#ff0000', text = 'Missed Critical alerts', fontsize = 12)
	stack_crit.set_tooltip('Critical: #val#<br>Total #total#')
	
	# Global chart
	chart = openFlashChart.template('Alerts KPI')
	chart.set_bg_colour('#c7c7c7')
	chart.set_tooltip(behaviour = 'hover')
	
	# Query DB to get values of last 5 kpis
	for stat in reversed(NagiosKPI.objects.order_by('-date')[0:5]):
		alert_warn_values = []
		alert_crit_values = []
		
		week = stat.date.isocalendar()[1]
		year = stat.date.isocalendar()[0]
		
		# Warning alerts
		warn_total = stat.alert_warn_total
		ack_warn_current = stat.alert_ack_warn_current
		ack_warn_total = stat.alert_ack_warn_total - ack_warn_current
		total_warn_missed = warn_total - ack_warn_total - ack_warn_current
		
		alert_warn_values.append(bar_stack_value(ack_warn_current, colour='#9e9e00', tooltip='#val# Current<br>Total #total#'))
		alert_warn_values.append(bar_stack_value(ack_warn_total, colour='#ffbf00', tooltip='#val# Detected<br>Total #total#'))
		alert_warn_values.append(bar_stack_value(total_warn_missed, colour='#ffff00', tooltip='#val# Missed<br>Total #total#'))
		
		# Critical alerts
		crit_total = stat.alert_crit_total
		ack_crit_current = stat.alert_ack_crit_current
		ack_crit_total = stat.alert_ack_crit_total - ack_crit_current
		total_crit_missed = crit_total - ack_crit_total - ack_crit_current
		
		alert_crit_values.append(bar_stack_value(ack_crit_current, colour='#ff3f00', tooltip='#val# Current<br>Total #total#'))
		alert_crit_values.append(bar_stack_value(ack_crit_total, colour='#760000', tooltip='#val# Detected<br>Total #total#'))
		alert_crit_values.append(bar_stack_value(total_crit_missed, colour='#ff0000', tooltip='#val# Missed<br>Total #total#'))
		
		# X Axis labels
		weeks.append('Week {0!s} - {1!s}'.format(week, year))
		
		# Compute MAX value that could be in graph for Y axis limit
		if stat.alert_warn_total > y_max_limit:
			y_max_limit = math.ceil(stat.alert_warn_total / 10.) * 10
		if stat.alert_crit_total > y_max_limit:
			y_max_limit = math.ceil(stat.alert_crit_total / 10.) * 10
		
		# Stack values
		stack_warn.append_stack(alert_warn_values)
		stack_crit.append_stack(alert_crit_values)
	
	chart.add_element(stack_warn)
	chart.add_element(stack_crit)
	chart.set_x_axis(labels = x_axis_labels(labels = weeks))
	chart.set_y_axis(max = y_max_limit, steps = 100)

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

# Create graph data for total monitored hosts and services stats, return json data
def total_stat_data(request):
	# Tests if we have value in DB
	if not NagiosKPI.objects.all():
		return HttpResponse('There is no data in database.')
	
	# Some var used in this view
	y_max_limit = 10
	hosts = []
	services = []
	months = range (1, 13)
	
	# Line chart
	line_hosts = Line(colour='#007900', text='Hosts')
	line_hosts.set_width(4)
	line_services = Line(colour='#0000ff', text='Services')
	line_services.set_width(4)
	
	# Global chart
	chart = openFlashChart.template('Total monitored hosts and services for year {0}'.format(date.today().year))
	chart.set_bg_colour('#ffffff')
	
	# Query DB to get values of current year
	for month in months:
		# Aggregate values per months
		hosts_in_month = NagiosKPI.objects.filter(date__month=month).aggregate(Avg('total_hosts'))['total_hosts__avg']
		services_in_month = NagiosKPI.objects.filter(date__month=month).aggregate(Avg('total_services'))['total_services__avg']
		
		try:
			hosts_in_month = int(math.ceil(hosts_in_month))
			services_in_month = int(math.ceil(services_in_month))
			
			# Compute MAX value that could be in graph for Y axis limit
			if hosts_in_month > y_max_limit:
				y_max_limit = hosts_in_month + 500
			if services_in_month > y_max_limit:
				y_max_limit = services_in_month + 500
		except TypeError:
			hosts_in_month = None
			services_in_month = None
		
		# Add Values (aggregated)
		hosts.append(hosts_in_month)
		services.append(services_in_month)
		
	# Add values to line graph
	line_hosts.set_values(hosts)
	line_services.set_values(services)
	
	chart.add_element(line_hosts)
	chart.add_element(line_services)
	chart.set_x_axis(labels = x_axis_labels(labels = [ str(m) for m in months ]))
	chart.set_y_axis(max = y_max_limit, steps = 1000)
	
	return HttpResponse(chart.encode())

