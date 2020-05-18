from django.urls import path, re_path

from .views import *

app_name = 'bp_manager'

urlpatterns = [
    path('create_team/', TeamCreateView.as_view(), name='create_team'),
    path('create_team/<int:id>', TeamCreateView.as_view(), name='create_team'),
    path('create_board/', BoardCreateView.as_view(), name='create_board'),
    path('create_board/<int:id>', BoardCreateView.as_view(), name='create_board_by_room'),
    path('create_process/', ProcessCreateView.as_view(), name='create_process'),
    path('create_process/<int:id>', ProcessCreateView.as_view(), name='create_process_by_board'),
    path('update_team/<int:pk>', TeamUpdateView.as_view(), name='update_team'),
    path('update_board/<int:pk>', BoardUpdateView.as_view(), name='update_board'),
    path('update_process/<int:pk>', ProcessUpdateView.as_view(), name='update_process'),
    path('delete_team/', TeamDeleteView.as_view(), name='delete_team'),
    path('delete_board/', BoardDeleteView.as_view(), name='delete_board'),
    path('delete_process/', ProcessDeleteView.as_view(), name='delete_process'),
    path('board/<int:id>', BoardDetail.as_view(), name='board_view'),
]
