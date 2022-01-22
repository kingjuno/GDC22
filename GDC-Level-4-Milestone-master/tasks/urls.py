from django.http import HttpResponseRedirect
from django.urls import path
from django.shortcuts import render

tasks = []
complete = []

def tasks_view(request):
    return render(request, 'tasks.html', {'tasks': tasks})

def add_task_view(request):
    tasks.append(request.GET.get('task'))
    return HttpResponseRedirect('/tasks')

def delete_task_view(request, index):
    del tasks[index-1]
    return HttpResponseRedirect('/tasks')

def completed_tasks_view(request):
    return render(request, 'completed_tasks.html', {'complete': complete})

def complete_task_view(request, index):
    complete.append(tasks[index-1])
    del tasks[index-1]
    return HttpResponseRedirect('/completed_tasks')

def all_tasks_view(request):
    return render(request, 'all_tasks.html', {'tasks': tasks+complete})

urlpatterns = [
    path('tasks/', tasks_view),
    path('add-task/', add_task_view),    
    path('delete-task/<int:index>/', delete_task_view),
    path('completed_tasks/', completed_tasks_view),
    path('complete_task/<int:index>/', complete_task_view),
    path('all_tasks/', all_tasks_view),
]
