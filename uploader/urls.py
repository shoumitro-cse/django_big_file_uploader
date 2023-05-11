from django.urls import path

from . import views

urlpatterns = [
    path('home/', views.home, name='home'),
    path('file_uploader/', views.FileUploaderAPIView.as_view(), name='file_uploader_api'),
]