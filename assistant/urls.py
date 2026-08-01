from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('google2f83435a64a9c20c.html', views.google_verification, name='google_verification'),
    path('api/command/', views.process_command_api, name='process_command_api'),
]
