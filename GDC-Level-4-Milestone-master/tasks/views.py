from django.shortcuts import render
from django.http import HttpResponseRedirect

tasks = []
complete = []


def tasks_view(request):
    return render(request, "tasks.html", {"tasks": tasks})


def add_task_view(request):
    tasks.append(request.GET.get("task"))
    return HttpResponseRedirect("/tasks")


def delete_task_view(request, index):
    del tasks[index - 1]
    return HttpResponseRedirect("/tasks")


def completed_tasks_view(request):
    return render(request, "completed_tasks.html", {"complete": complete})


def complete_task_view(request, index):
    complete.append(tasks[index - 1])
    del tasks[index - 1]
    return HttpResponseRedirect("/completed_tasks")


def all_tasks_view(request):
    return render(request, "all_tasks.html", {"tasks": tasks + complete})
