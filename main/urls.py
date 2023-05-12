from os import path
from django.urls import path,include, re_path as url
from . import views

urlpatterns = [
    path('',views.index,name='index'),   
    path('index/',views.index,name='index'),   
    path('about/',views.about,name='about'),   
    path('event/',views.event,name='event'), 
    path('chefs/',views.chefs,name='chefs'), 
    path('gallery/',views.gellery,name='gallery'), 
    path('contact/',views.contact,name='contact'), 
   ]
