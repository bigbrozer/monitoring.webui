# Reporting app views

from django.shortcuts import render_to_response

def status(request):
	title = 'Status overview for active alerts'
	return render_to_response('reporting/status.html', {'title': title})
