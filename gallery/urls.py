from os import path
from django.urls import path,include, re_path as url
from .views import *
from . import views

urlpatterns = [

    path('gallery/', photo_gallery, name='photo_gallery'),
    path('add_photo/', add_photo,name='add_photo'),    
    path('edit_photo/<str:pid>',edit_photo , name='edit_photo'), 
    path('photo_list/',photo_list , name='photo_list'),
    #path('save_edit_photo/',save_edit_photo , name='save_edit_photo'), 
    path('delete_photo/',delete_photo , name='delete_photo'), 

    path('add_photo_category/', add_photo_category,name='add_photo_category'), 
    path('edit_photo_category/',edit_photo_category , name='edit_photo_category'),
    path('photo_category_list/', photo_category_list,name='photo_category_list'),
    path('save_edit_photo_category/',save_edit_photo_category , name='save_edit_photo_category'),
    path('delete_photo_category/',delete_photo_category , name='delete_photo_category'), 

    ]
