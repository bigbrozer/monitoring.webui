# Highlights app models

from django.db import models

# Represent a project we are working on (Colisee, MIT, FCS...)
class Project(models.Model):
	name = models.CharField(max_length=64, help_text='Project name, ex: FCS, Domain Controllers, ...')
	
	def __unicode__(self):
		return self.name

# Represent a highlight
class Highlight(models.Model):
	title = models.CharField(max_length=128, help_text='Title of the highlight, should be short.')
	description = models.TextField(help_text='Enter a detailed description of the highlight.')
	date = models.DateTimeField(auto_now_add=True)
	project = models.ForeignKey(Project, help_text='Select for which project this highlight is associated.')
	
	def __unicode__(self):
		return self.title
