from os import path
from django.urls import path,include, re_path as url
from blog.views import *
urlpatterns = [

    path('blog/',blog,name='blog'),   
    path('post_blog/',post_blog,name='post_blog'),
    path('post_comment/',post_comment,name='post_comment'),
    path('del_comment/',del_comment,name='del_comment'),    
    path('del_blog/',del_blog,name='del_blog'), 
    path('del_blog_category/',del_blog_category,name='del_blog_category'),       
    path('edit_blog/',edit_blog,name='edit_blog'),
    path('press_like/',press_like,name='press_like'),    
    path('save_edit_blog/',save_edit_blog,name='save_edit_blog'),    
    path('blog_detail/',blog_detail,name='blog_detail'),        
    path('save_blog/', save_blog,name='save_blog'),  
    path('add_blog_category/', add_blog_category,
        name='add_blog_category'),    
    path('edit_blog_category/',edit_blog_category , name='edit_blog_category'),         
    path('save_edit_blog_category/',save_edit_blog_category , name='save_edit_blog_category'),         
    path('search_title/', search_title, name='search_title'),        
    url(r'^(?P<category_slug>[-\w]+)/$',blog,name='blog_list_by_category'),        
    url(r'^(?P<blog_id>\d+)/(?P<slug>[-\w]+)/$',
        blog_detail,
        name='blog_detail'),
    ]
