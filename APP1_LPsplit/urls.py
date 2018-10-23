from django.urls import path,re_path

from . import views

app_name = 'APP1'

urlpatterns = [
    re_path(r'StapleSelected(\d+)/',views.StapleSelected),
    path(r'Recommend/',views.Recommend),
    path(r'Staple/',views.Staple),
    path('', views.Index, name='index'),
]