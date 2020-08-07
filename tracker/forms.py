from django import forms
from .models import Project,TaskTracker
from django.contrib.admin.widgets import AdminDateWidget

class ProjectModelForm(forms.ModelForm):
	class Meta:
		model  = Project
		fields = ['project']

		widgets = {
		'project':forms.TextInput(attrs={'class':'form-control'})
		}





class TaskTrackerModelForm(forms.ModelForm):
	class Meta:
		model  = TaskTracker
		fields = ['task_name','project']

		widgets = {
		'task_name':forms.TextInput(attrs={'class':'form-control','id':'task-me'}),
		'project': forms.Select(attrs={'class':'form-control','id':'project-me'})
		}

	def __init__(self, *args, **kwargs):
		self.user = kwargs.pop('user', None)
		super(TaskTrackerModelForm, self).__init__(*args, **kwargs)
		self.fields['project'].queryset = Project.objects.filter(user = self.user)



class AnalyzeModelForm(forms.ModelForm):
	"""This model form provides user the ability to
	 select a project and analyze it progress"""

	class Meta:
		model  = TaskTracker
		fields = ['project']

		widgets = {
		'project': forms.Select(attrs={'class':'form-control','id':'project-me'})
		}

	def __init__(self, *args, **kwargs):
		self.user = kwargs.pop('user', None)
		super(AnalyzeModelForm, self).__init__(*args, **kwargs)
		self.fields['project'].queryset = Project.objects.filter(user = self.user)


class DatePickerForm(forms.Form):
	date   = forms.DateField(widget=forms.TextInput(attrs={'class': 'form-control','id':'datepicker','placeholder':'Please Select a Date'}))
