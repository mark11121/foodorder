import os
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from menu.models import *

# Create your views here.
def index(request):
    return render(request,'main/index.html')

def about(request):
    return render(request,'main/about.html')



def event(request):
    return render(request,'main/event.html')

def chefs(request):
    return render(request,'main/chefs.html')

def gellery(request):
    return render(request,'main/gellery.html')

def contact(request):
    return render(request,'main/contact.html')

def contact(request):
    return render(request,'main/contact.html')



