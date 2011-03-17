# Downtime app views

from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.template import RequestContext

# Forms imports
from optools.apps.downtime.forms import ScheduleDowntimeForm

# View that render the form to schedule a downtime
@login_required
def schedule(request):
	title = 'Schedule a downtime in Nagios'
	if request.POST:
		form = ScheduleDowntimeForm(request.POST)
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
