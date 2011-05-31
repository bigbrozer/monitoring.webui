# Downtime app views

from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.core.urlresolvers import reverse

# Forms imports
from optools.apps.downtime.forms import ScheduleDowntimeForm

# Nagios handlers
from optools.apps.downtime.commands import ScheduleFullDowntime

# View that render the form to schedule a downtime
@login_required
def schedule(request):
	title = 'Schedule a downtime in Nagios'
	if request.POST:
		form = ScheduleDowntimeForm(request.POST)
		if form.is_valid():
			downtime_descr = form.cleaned_data['downtime_descr']
			hosts = form.cleaned_data['host_list'].split(',')
			start_period = form.cleaned_data['start_period']
			end_period = form.cleaned_data['end_period']

			for host in hosts:
				# Skip blank host (skip last comma where host name is empty)
				if not host:
					continue
				command = ScheduleFullDowntime(host, start_period, end_period, request.user.username, downtime_descr)
				command.send()
				# TODO: add some security, warn if command was not successfull

			return HttpResponse('Successfully created downtime for hosts.')
	else:
		form = ScheduleDowntimeForm()
	
	return render_to_response(
			'downtime/schedule_downtime.html',
			{
				'title': title,
				'form': form,
			},
			context_instance=RequestContext(request)
		)

