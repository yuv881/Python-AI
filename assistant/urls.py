from django.urls import path
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('robots.txt', TemplateView.as_view(template_name='robots.txt', content_type='text/plain'), name='robots_txt'),
    path('google2f83435a64a9c20c.html', views.google_verification, name='google_verification'),
    path('api/command/', views.process_command_api, name='process_command_api'),
]

