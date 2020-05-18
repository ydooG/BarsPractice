from django.urls import path
from . import views

app_name = 'vcs'

urlpatterns = [
    path('rep/<str:id>', views.RepositoryView.as_view(), name='rep'),
    path('create-rep/', views.create_rep, name='create_rep')
]
