from django.urls import path

from . import views

urlpatterns = [
    path('file_uploader/', views.file_uploader, name='file_uploader'),
]