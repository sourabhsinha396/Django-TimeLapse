from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import datetime
from django.core.paginator import Paginator


# Imports from this app
from .models import Project,TaskTracker
from .forms import (ProjectModelForm,TaskTrackerModelForm,
					AnalyzeModelForm,DatePickerForm)

@login_required
def homepage(request):
	"""Function Based view to get info about what projects the user is working on"""
	already_existing_projects = Project.objects.filter(user=request.user)

	if request.method == "POST":
		form = ProjectModelForm(request.POST)  # instantiating the model form with the post data
		if form.is_valid():
			form_obj = form.save(commit=False)
			form_obj.user = request.user
			form_obj.save()
			messages.success(request,"Successfully created the project in your project list")
		else:
			messages.error(request,form.errors)
		context = {'form':form,'already_existing_projects':already_existing_projects}
		return render(request,'tracker/homepage.html',context)

	else:
		form = ProjectModelForm()
		context = {'form':form,'already_existing_projects':already_existing_projects}
		return render(request,'tracker/homepage.html',context)

@login_required
def task_tracker(request):
	""" This function handles the tracking of tasks related to diff. projects"""
	user = request.user 

	if request.method == "GET":
		active_task = TaskTracker.objects.filter(user=user,end_time=None).order_by('-start_time')
		if active_task.exists():
			print("active",active_task.first())
			instance = active_task.first()
			form = TaskTrackerModelForm(user=user,instance=instance)
		else:
			form = TaskTrackerModelForm(user=user) 
		# passed the user object so as to filter the Project object in __init__(in forms.py), which has the same user as current user.
		context = {'form':form}
		return render(request,'tracker/task_tracker.html',context)


def start_tracking(request):
	post_data_task_name    = request.POST.get('task_name')
	post_data_project_name = request.POST.get('project')
	project_obj            = Project.objects.get(id=post_data_project_name)

	if request.method == "POST":
		print(request.POST)
		check_existance = TaskTracker.objects.filter(user=request.user,task_name=post_data_task_name,
											project=post_data_project_name,
											end_time=None)
		if check_existance.exists():
			return JsonResponse({'msg':'This task already exists,Please End it first'})

		try:
			TaskTracker.objects.create(user=request.user,
										task_name=post_data_task_name,
										project = project_obj,
										start_time = datetime.now()
										)
			print("Done Saving")
			return JsonResponse({'msg':'{} started successfully'.format(post_data_task_name),'startTimer':True})
		except:
			return JsonResponse({'msg':'some error occured'})


def end_tracking(request):
	post_data_task_name    = request.POST.get('task_name')
	post_data_project_name = request.POST.get('project')
	user                   = request.user
	project_obj            = Project.objects.get(id=post_data_project_name)
	check_existing = TaskTracker.objects.filter(user=user,task_name=post_data_task_name,
								project=project_obj,end_time=None).order_by('-start_time')
	if check_existing.exists():
		instance = check_existing.first()
		instance.end_time = datetime.now()
		instance.save()
		print(instance)
		return JsonResponse({'msg':'Successfully ended the task tracking'})
	else:
		return JsonResponse({'msg':'The task has already ended'})



def track_my_progress(request):
	user              = request.user
	if request.method == "POST":
		project       = request.POST.get('project')
		ended_tasks   = TaskTracker.objects.filter(user=user,project=project)
		form    = AnalyzeModelForm(request.POST)
		context = {'object_list':ended_tasks,'form':form}
		return render(request,'tracker/analyze.html',context)

	if request.method == "GET":
		form 		  = AnalyzeModelForm(user=user)
		context       = {'form':form}
		return render(request,'tracker/analyze.html',context)


def analyze_by_date(request):
	user              = request.user
	ended_tasks       = "Tasks"
	if request.method == "POST":
		form          = DatePickerForm(request.POST)
		date          = request.POST.get('date')
		if form.is_valid():
			date          = form.cleaned_data.get('date')  
		ended_tasks   = TaskTracker.objects.filter(user=user,start_time__date__lte=date)
		paginator = Paginator(ended_tasks,3) 
		page_number = request.POST.get('page')
		page_obj = paginator.get_page(page_number)
		context = {'object_list':page_obj,'date':date,'form':form}
		return render(request,'tracker/analyze_by_date.html',context)

	if request.method == "GET":
		form    = DatePickerForm()
		context = {'form':form}
		return render(request,'tracker/analyze_by_date.html',context)
