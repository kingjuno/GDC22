from django.contrib.auth.models import User
from django.views import View
from django_filters.rest_framework import (
    BooleanFilter,
    CharFilter,
    ChoiceFilter,
    DateFilter,
    DjangoFilterBackend,
    FilterSet,
    ModelChoiceFilter,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.serializers import ModelSerializer
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from .models import STATUS_CHOICES, Task, TaskHistory


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ("first_name", "last_name", "username")


class TaskSerializer(ModelSerializer):

    user = UserSerializer(read_only=True)

    class Meta:
        model = Task
        fields = ["title", "description", "completed", "user"]


class TaskFilter(FilterSet):
    title = CharFilter(lookup_expr="icontains")
    status = ChoiceFilter(choices=STATUS_CHOICES)
    completed = BooleanFilter()


class TaskViewSet(ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    permission_classes = (IsAuthenticated,)

    filter_backends = (DjangoFilterBackend,)
    filterset_class = TaskFilter

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user, deleted=False)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class TaskListAPI(View):
    def get(self, request):
        tasks = Task.objects.filter(deleted=False)
        data = TaskSerializer(tasks, many=True).data
        return Response({"tasks": data})


class TaskHistorySerializer(ModelSerializer):
    class Meta:
        model = TaskHistory
        fields = "__all__"



class TaskHistoryFilter(FilterSet):
    task = ModelChoiceFilter(queryset=Task.objects.all())
    new_status = ChoiceFilter(choices=STATUS_CHOICES)
    old_status = ChoiceFilter(choices=STATUS_CHOICES)
    updated_date = DateFilter(lookup_expr="date")
    # something like 2022-02-12 would be enough for this to work


class TaskHistoryViewSet(ReadOnlyModelViewSet):
    queryset = TaskHistory.objects.all()
    serializer_class = TaskHistorySerializer

    permission_classes = (IsAuthenticated,)

    filter_backends = (DjangoFilterBackend,)
    filterset_class = TaskHistoryFilter

    def get_queryset(self):
        return TaskHistory.objects.filter(task__user=self.request.user)
