from django.urls import path,re_path

from . import views

app_name = 'APP2'

urlpatterns = [
    path(r'downloadexample/',views.downloadexample),
    path(r'uploads/',views.uploads),
    path('', views.index, name='index'),
]