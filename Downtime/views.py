# Downtime app views

from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.template import RequestContext

@login_required
def schedule(request):
	title = 'Schedule a downtime in Nagios'
	return render_to_response('downtime/schedule_downtime.html', {'title': title}, context_instance=RequestContext(request))
