from django.urls import path

from .views import *
from .apiviews import *
from django.contrib.auth.views import LogoutView
from rest_framework.routers import SimpleRouter
from rest_framework_nested.routers import NestedSimpleRouter

from tasks.apiviews import *

router = SimpleRouter()
router.register('api/task', TaskViewSet)

hist_router = NestedSimpleRouter(router, 'api/task', lookup='task')
hist_router.register('history', TaskHistoryViewSet)
urlpatterns = [
    path('', GenericTaskView.as_view()),
    path('taskapi/', TaskListAPI.as_view()),
    path('tasks/', GenericTaskView.as_view()),
    path('create-task/', GenericTaskCreateView.as_view()),
    path('update-task/<pk>', GenericTaskUpdateView.as_view()),
    path('detail-task/<pk>', GenericTaskDetailView.as_view()),
    path('delete-task/<pk>', GenericTaskDeleteView.as_view()),
    path('sessiontest/', session_storage_view),
    path('user/signup/', UserCreateView.as_view()),
    path('user/login/', UserLoginView.as_view()),
    path('user/logout/', LogoutView.as_view()),
] + router.urls + hist_router.urls