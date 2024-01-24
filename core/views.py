from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request, 'index.html')

def faq(request):
    return render(request, 'faq.html')

def about(request):
    return render(request, 'about.html')