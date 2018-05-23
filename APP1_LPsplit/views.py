# _*_coding: utf-8 _*_

from django.shortcuts import render

def index(request):
    return render(request,'APP1_LPsplit/index.html')
