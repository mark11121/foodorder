from os import path
from django.urls import path,include, re_path as url
from blog.views import *
urlpatterns = [

    path('blog/',blog,name='blog'),   
    path('add_blog/',add_blog,name='add_blog'),
    path('post_comment/',post_comment,name='post_comment'),
    path('edit_blog/<str:pid>',edit_blog,name='edit_blog'),
    path('blog_list/',blog_list , name='blog_list'),
    #path('save_edit_blog/',save_edit_blog,name='save_edit_blog'), 
    path('delete_blog/',delete_blog,name='delete_blog'), 
    path('blog_detail/',blog_detail,name='blog_detail'),

    path('add_blog_category/',add_blog_category,name='add_blog_category'),    
    path('edit_blog_category/',edit_blog_category , name='edit_blog_category'),
    path('blog_category_list/',blog_category_list,name='blog_category_list'),
    path('save_edit_blog_category/',save_edit_blog_category , name='save_edit_blog_category'),
    path('delete_blog_category/',delete_blog_category,name='delete_blog_category'),

    path('del_comment/',del_comment,name='del_comment'),    
    path('press_like/',press_like,name='press_like'),          
    path('press_hate/',press_hate,name='press_hate'), 
    path('search_title/', search_title, name='search_title'),  



    url(r'^(?P<category_slug>[-\w]+)/$',blog,name='blog_list_by_category'),        
    url(r'^(?P<blog_id>\d+)/(?P<slug>[-\w]+)/$',blog_detail,name='blog_detail'),
    ]
