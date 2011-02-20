# Downtime app views

from django.shortcuts import render_to_response

def schedule(request):
	title = 'Schedule a downtime in Nagios'
	return render_to_response('downtime/schedule_downtime.html', {'title': title})
