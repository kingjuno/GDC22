from django.urls import path

from .views import *

urlpatterns = [
    path('', tasks_view),
    path('tasks/', tasks_view),
    path('add-task/', add_task_view),    
    path('delete-task/<int:index>/', delete_task_view),
    path('completed_tasks/', completed_tasks_view),
    path('complete_task/<int:index>/', complete_task_view),
    path('all_tasks/', all_tasks_view),
]
