# Reporting app views

# Django imports
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.template import RequestContext
from django.db.models import Avg

# Models
from optools.apps.reporting.models import NagiosKPI

# Utility
import math
from datetime import date

# The view that show graph about stats
def stats(request):
	template_context = {
		'title': 'Nagios KPI',
	}
	
	return render_to_response('reporting/status.html', template_context, context_instance=RequestContext(request))

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
	procedure.set_on_click(request.build_absolute_uri('/~django/reports/services_procedure_in_nagios.csv'))

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
		kpi_comments = [ kpi.comment for kpi in NagiosKPI.objects.filter(date__month=month) ]
		
		try:
			hosts_in_month = int(math.ceil(hosts_in_month))
			services_in_month = int(math.ceil(services_in_month))
			
			# Compute MAX value that could be in graph for Y axis limit
			if hosts_in_month > y_max_limit:
				y_max_limit = hosts_in_month + 500
			if services_in_month > y_max_limit:
				y_max_limit = services_in_month + 500

			# Add Values as dot_value in graph
			remark = ''
			if any(kpi_comments):
				remark = '<br>Remarks:<br>'
			for comment in kpi_comments:
				if comment:
					remark += '{0}<br>'.format(comment)
			
			hosts.append(dot_value(hosts_in_month, colour='#0000FF', tooltip='Value: #val#{0}'.format(remark)))
			services.append(dot_value(services_in_month, colour='#00FF00', tooltip='Value: #val#{0}'.format(remark)))
		except TypeError:
			# Add null value
			hosts.append(None)
			services.append(None)
		
	# Add values to line graph
	line_hosts.set_values(hosts)
	line_services.set_values(services)
	
	chart.add_element(line_hosts)
	chart.add_element(line_services)
	chart.set_x_axis(labels = x_axis_labels(labels = [ str(m) for m in months ]))
	chart.set_y_axis(max = y_max_limit, steps = 1000)
	
	return HttpResponse(chart.encode())

