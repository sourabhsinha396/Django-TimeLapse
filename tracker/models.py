from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Project(models.Model):
	"""We are going to use this model
	 as a dropdown select in TaskTracker Model
	 This also enables us to not to hardcode tasks in dropdown."""

	user         = models.ForeignKey(User,on_delete = models.CASCADE)
	project      = models.CharField(max_length=100,db_index=True)

	def __str__(self):
		return str(self.project)[:30]




class TaskTracker(models.Model):
	"""This is the actual Model which tracks time for the user"""

	user         = models.ForeignKey(User,on_delete=models.CASCADE)
	task_name    = models.CharField(max_length=255)
	project      = models.ForeignKey(Project,on_delete=models.SET_NULL,
									null=True,db_index=True)
	start_time   = models.DateTimeField()
	end_time     = models.DateTimeField(blank=True,null=True)

	def __str__(self):
		return self.task_name

	def convert_sec(self,seconds):
		seconds = seconds % (24 * 3600) 
		hour = seconds // 3600
		seconds %= 3600
		minutes = seconds // 60
		seconds %= 60
		return "%d Hour:%02d Minutes:%02d Seconds" % (hour, minutes, seconds) 

	def get_time_difference(self):
		if not self.end_time:
			return "Ongoing Task"
		return self.convert_sec((self.end_time - self.start_time).total_seconds())





