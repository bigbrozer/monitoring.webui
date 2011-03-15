# Downtime app views

from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django import forms

# Forms classes

# Schedule a downtime form
class ScheduleDowntimeForm(forms.Form):
	downtime_name = forms.CharField(label='Downtime name', help_text='Name of downtime, ex: PDM Backup', max_length=100)
	search_host = forms.CharField(label='Search host', help_text='Search host to schedule', required=False)
	host_list = forms.CharField(label='Host name list', help_text='Enter host names separated by comma', widget=forms.Textarea)
	start_period = forms.DateTimeField(label='Start period', help_text='Start date for the downtime')
	end_period = forms.DateTimeField(label='End period', help_text='End date for the downtime')
	is_recurrent = forms.BooleanField()
	
	# Recurrency options form
	start_time = forms.TimeField(label='Start time', help_text='Start hour for the recurrent downtime')
	end_time = forms.TimeField(label='End time', help_text='End hour for the recurrent downtime')
	is_monday = forms.BooleanField(label='Monday')
	is_tuesday = forms.BooleanField(label='Tuesday')
	is_wednesday = forms.BooleanField(label='Wednesday')
	is_thursday = forms.BooleanField(label='Thursday')
	is_friday = forms.BooleanField(label='Friday')
	is_saturday = forms.BooleanField(label='Saturday')
	is_sunday = forms.BooleanField(label='Sunday')

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
