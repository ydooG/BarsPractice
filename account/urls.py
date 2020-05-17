from django.urls import path

from account.decorators import manager_perm_required
from . import views
from django.contrib.auth import views as auth_views


app_name = 'account'

urlpatterns = [
    path('', views.root, name='root'),
    path('reg/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('create-room/', views.create_room, name='create_room'),
    path('room/', views.room, name='room'),
    path('profile/<str:username>', views.ProfileView.as_view(), name='profile'),
    path('add-staff/', views.add_staff, name='add_staff'),
    path('delete/<int:pk>', manager_perm_required(views.UserDelete.as_view()), name='delete_user'),
]
