from django.urls import path
from . import views

app_name = 'vcs'

urlpatterns = [
    path('rep/<int:id>', views.RepositoryView.as_view(), name='rep'),
    path('create-rep/', views.CreateRepositoryView.as_view(), name='create_rep')
]
