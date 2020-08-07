from django.urls import path
from .import views


urlpatterns = [
	path('',views.homepage,name="homepage"),
	path('track/',views.task_tracker,name="task_tracker"),
	path('start/',views.start_tracking,name="start"),
	path('end/',views.end_tracking,name="end"),
	path('analyze/',views.track_my_progress,name="analyze"),
	path('analyze-date/',views.analyze_by_date,name="analyze_date"),
]