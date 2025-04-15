from django.shortcuts import render

def login(request):
    return render(request, 'Login.html', {})

def home(request):
    return render(request, 'Home.html', {})
