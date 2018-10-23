from django.shortcuts import render

# Create your views here.
def Index(request):
    return render(request,'APP0_Homepage/index.html')