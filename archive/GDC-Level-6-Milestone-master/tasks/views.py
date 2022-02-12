from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator
from django.forms import ModelForm
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.db import transaction
from itsdangerous import exc

from tasks.models import Task


class AuthorisedTaskManager(LoginRequiredMixin):
    def get_queryset(self):
        return Task.objects.filter(deleted=False, user=self.request.user)


class UserLoginView(LoginView):
    template_name = "user_login.html"


class UserCreateView(CreateView):
    form_class = UserCreationForm
    template_name = "user_create.html"
    success_url = "/user/login/"


def session_storage_view(request):
    total_views = request.session.get("total_views", 0)
    request.session["total_views"] = total_views + 1
    return HttpResponse(f"Total views: {total_views} and user is {request.user}")


class GenericTaskDeleteView(AuthorisedTaskManager, DeleteView):
    model = Task
    template_name = "task_delete.html"
    success_url = "/tasks"


class GenericTaskDetailView(AuthorisedTaskManager, DetailView):
    model = Task
    template_name = "task_detail.html"


def set_priority(priority, user):
    tasks = []
    try:
        task = Task.objects.select_for_update().get(
            priority=priority, user=user, deleted=False, completed=False
        )
    except Task.DoesNotExist:
        return 
    with transaction.atomic():
        while task.priority == priority:
            priority += 1
            task.priority += 1
            tasks.append(task)
            try:
                task = Task.objects.select_for_update().get(
                    priority=priority, user=user, deleted=False, completed=False
                )
            except Task.DoesNotExist:
                break
    Task.objects.bulk_update(tasks, ["priority"])


class GenericTaskUpdateView(AuthorisedTaskManager, UpdateView):
    model = Task
    template_name = "task_update.html"
    fields = ["title", "description", "priority", "completed"]
    success_url = "/tasks"

    def form_valid(self, form):
        if form.has_changed():
            if "priority" in form.changed_data or (
                "completed" in form.changed_data and not form.instance.completed
            ):
                set_priority(form.instance.priority, self.request.user)
        self.object = form.save()
        return HttpResponseRedirect(self.get_success_url())


class GenericTaskCreateView(CreateView):
    model = Task
    fields = ("title", "description", "priority", "completed")
    template_name = "task_create.html"
    success_url = "/tasks"

    def form_valid(self, form):
        self.object = form.save()
        self.object.user = self.request.user
        if form.cleaned_data["completed"] == False:
            priority = self.object.priority
            set_priority(priority, self.request.user)
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


class GenericTaskView(LoginRequiredMixin, ListView):
    queryset = Task.objects.filter(deleted=False)
    template_name = "tasks.html"
    context_object_name = "tasks"

    def get_queryset(self):
        search_term = self.request.GET.get("search")
        tasks = Task.objects.filter(deleted=False, user=self.request.user)
        completed = Task.objects.filter(
            deleted=False, user=self.request.user, completed=True
        )
        if search_term:
            tasks = tasks.filter(title__icontains=search_term)
        return tasks, completed
