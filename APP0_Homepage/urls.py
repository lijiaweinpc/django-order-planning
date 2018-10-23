from django.urls import path,re_path

from . import views

app_name = 'APP0'

urlpatterns = [
    path('', views.Index, name='index'),
]