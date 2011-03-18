# Downtime app views

from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.core.urlresolvers import reverse

# Forms imports
from optools.apps.downtime.forms import ScheduleDowntimeForm

# View that render the form to schedule a downtime
@login_required
def schedule(request):
	title = 'Schedule a downtime in Nagios'
	if request.POST:
		form = ScheduleDowntimeForm(request.POST)
		if form.is_valid():
			return HttpResponseRedirect(reverse('optools.apps.downtime.views.show', args=(1,)))
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

# Show downtime detail view
def show(request, downtime_id):
	return HttpResponse('Successfully created downtime with id %s.' % downtime_id)
