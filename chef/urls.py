from os import path
from django.urls import path,include, re_path as url
from .views import *
from . import views

urlpatterns = [

    path('chef/',chef,name='chef'),   
    path('add_chef/',add_chef,name='add_chef'), 
    path('del_chef/',del_chef,name='del_chef'), 
    path('edit_chef/',edit_chef,name='edit_chef'),
    path('save_edit_chef/',save_edit_chef,name='save_edit_chef'),
    path('chef_list/',chef_list , name='chef_list'),
    path('search_chef/',chef_list , name='search_chef'), 

    ]
