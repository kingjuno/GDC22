from django.shortcuts import render
from django.http import HttpResponseRedirect

from tasks.models import Task

def tasks_view(request):
    search_term = request.GET.get("search")
    tasks = Task.objects.filter(deleted = False, completed = False)
    if search_term:
        tasks = tasks.filter(title = search_term)
    return render(request, "tasks.html", {"tasks": tasks})


def add_task_view(request):
    task_value = request.GET.get("task")
    task_obj = Task(title = task_value)
    task_obj.save()
    return HttpResponseRedirect("/tasks")


def delete_task_view(request, index):
    Task.objects.filter(id = index).update(deleted = True)
    return HttpResponseRedirect("/tasks")


def completed_tasks_view(request):
    complete = Task.objects.filter(deleted = False, completed = True)
    return render(request, "completed_tasks.html", {"complete": complete})


def complete_task_view(request, index):
    Task.objects.filter(id = index).update(completed = True)
    return HttpResponseRedirect("/completed_tasks")


def all_tasks_view(request):
    tasks = Task.objects.filter(deleted = False)
    return render(request, "all_tasks.html", {"tasks": tasks})
