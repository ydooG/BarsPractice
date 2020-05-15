from django.urls import path, re_path

from .views import *

app_name = 'task_manager'

urlpatterns = [
    path('create_task/', TaskCreateView.as_view(), name='create_task'),
    path('create_task/<int:id>', TaskCreateView.as_view(), name='create_task_by_process'),
    path('update_task/<int:pk>', TaskUpdateView.as_view(), name='update_task'),
    path('delete_task/', TaskDeleteView.as_view(), name='delete_task'),
    path('start_task/', StartTask.as_view(), name='start_task'),

]
