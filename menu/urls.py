from os import path
from django.urls import path,include, re_path as url
from .views import *
urlpatterns = [

    path('menu/',menu,name='menu'),   
    path('add_menu_item/', add_menu_item,name='add_menu_item'),  
    path('edit_menu/<str:pid>',edit_menu , name='edit_menu'), 
    path('menu_list/',menu_list , name='menu_list'),
    path('menu_detail/',menu_detail , name='menu_detail'),
    #path('save_edit_menu/',save_edit_menu , name='save_edit_menu'),
    path('del_menu/',del_menu , name='del_menu'),


    path('add_menu_category/', add_menu_category,name='add_menu_category'),    
    path('edit_menu_category/',edit_menu_category , name='edit_menu_category'), 
    path('menu_category_list/', menu_category_list,name='menu_category_list'),
    path('save_edit_menu_category/',save_edit_menu_category , name='save_edit_menu_category'), 
    path('del_menu_category/',del_menu_category , name='del_menu_category'),               
    url(r'^(?P<menu_category_slug>[-\w]+)/$',menu,name='menu_list_by_category'),        
    url(r'^(?P<menu_id>\d+)/(?P<slug>[-\w]+)/$',menu_detail,name='menu_detail'),
    ]
