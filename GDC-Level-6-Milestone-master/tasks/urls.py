from django.urls import path

from .views import *
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', GenericTaskView.as_view()),
    path('tasks/', GenericTaskView.as_view()),
    path('create-task/', GenericTaskCreateView.as_view()),
    path('update-task/<pk>', GenericTaskUpdateView.as_view()),
    path('detail-task/<pk>', GenericTaskDetailView.as_view()),
    path('delete-task/<pk>', GenericTaskDeleteView.as_view()),
    path('sessiontest/', session_storage_view),
    path('user/signup/', UserCreateView.as_view()),
    path('user/login/', UserLoginView.as_view()),
    path('user/logout/', LogoutView.as_view()),
]
