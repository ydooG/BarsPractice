from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('', include('account.urls', namespace='account')),
    path('chat/', include('chat.urls', namespace='chat')),
    path('task_manager/', include('task_manager.urls', namespace='task_manager')),
    path('bp_manager/', include('bp_manager.urls', namespace='bp_manager')),
    path('admin/', admin.site.urls),
]
