# Downtime app forms

from django import forms

# Utilities
from datetime import datetime

# Schedule a downtime form
class ScheduleDowntimeForm(forms.Form):
	downtime_name = forms.CharField(label='Downtime name', help_text='Name of downtime, ex: PDM Backup', max_length=100)
	host_list = forms.CharField(label='Host name list', help_text='Enter host names separated by comma', widget=forms.Textarea)
	start_period = forms.DateTimeField(label='Start period', help_text='Start date for the downtime',
		required=False, initial=datetime.strftime(datetime.now(), '%m/%d/%Y %H:%M'))
	end_period = forms.DateTimeField(label='End period', help_text='End date for the downtime', required=False)
	is_recurrent = forms.BooleanField(label='Recurrent', help_text='Is it a recurrent downtime ?', required=False)
	
	# Recurrency options form
	start_time = forms.TimeField(label='Start time', help_text='Start hour for the recurrent downtime', required=False)
	end_time = forms.TimeField(label='End time', help_text='End hour for the recurrent downtime', required=False)
	is_monday = forms.BooleanField(label='Monday', required=False)
	is_tuesday = forms.BooleanField(label='Tuesday', required=False)
	is_wednesday = forms.BooleanField(label='Wednesday', required=False)
	is_thursday = forms.BooleanField(label='Thursday', required=False)
	is_friday = forms.BooleanField(label='Friday', required=False)
	is_saturday = forms.BooleanField(label='Saturday', required=False)
	is_sunday = forms.BooleanField(label='Sunday', required=False)
	
	# Form Validation
	def clean(self):
		cleaned_data = self.cleaned_data
		is_recurrent = cleaned_data.get('is_recurrent')
		start_period = cleaned_data.get('start_period')
		end_period = cleaned_data.get('end_period')
		
		# Recurrency options
		days = {
			'monday'	: cleaned_data.get('is_monday'),
			'tuesday'	: cleaned_data.get('is_tuesday'),
			'wednesday'	: cleaned_data.get('is_wednesday'),
			'thursday'	: cleaned_data.get('is_thursday'),
			'friday'	: cleaned_data.get('is_friday'),
			'saturday'	: cleaned_data.get('is_saturday'),
			'sunday'	: cleaned_data.get('is_sunday'),
		}
		start_time = cleaned_data.get('start_time')
		end_time = cleaned_data.get('end_time')
		
		# Non recurrent downtime
		if not is_recurrent:
			# Check that user provided start / end period value
			if not start_period:
				self._errors['start_period'] = self.error_class(
					['Please specify a start period for non recurrent downtime.']
				)
				del cleaned_data['start_period']
			if not end_period:
				self._errors['end_period'] = self.error_class(
					['Please specify a end period for non recurrent downtime.']
				)				
				del cleaned_data['end_period']
			
			# Check that end period is ALWAYS highter than start period
			if start_period and end_period and start_period > end_period:
				raise forms.ValidationError('Start period should be defined before end period.')
			
			# Check that end period is not defined in the past
			if end_period and end_period <= datetime.now():
				raise forms.ValidationError('End period should be defined in the future.')
		
		# Recurrent downtime
		else:
			# Check that user provided at least one day when to schedule downtime
			if not any(days.values()):
				raise forms.ValidationError('Please select at least a day for recurrent downtime.')
			
			# Check that user provided start / end time value
			if not start_time:
				self._errors['start_time'] = self.error_class(
					['Please specify a start time for recurrent downtime.']
				)
				del cleaned_data['start_time']
			if not end_time:
				self._errors['end_time'] = self.error_class(
					['Please specify a end time for recurrent downtime.']
				)				
				del cleaned_data['end_time']
			
			# Check that end time is ALWAYS highter than start time
			if start_time > end_time:
				raise forms.ValidationError('Start time should be defined before end time.')
		
		return cleaned_data
