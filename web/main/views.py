from django.shortcuts import render

# Create your views here.

def dance(request):
    return render(request, 'home.html')