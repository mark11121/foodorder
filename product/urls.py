from os import path
from django.urls import path,include, re_path as url
from .views import *
from . import views
   
urlpatterns = [

    path('product_menu/',product_menu,name='product_menu'),  

    path('product/',product,name='product'),  
    path('add_product/', add_product,name='add_product'),
    path('edit_product/<str:pid>',edit_product , name='edit_product'), 
    path('product_list/',product_list , name='product_list'),
    #path('save_edit_product/',save_edit_product , name='save_edit_product'), 
    path('delete_product/',delete_product , name='delete_product'), 
    path('product_detail/',product_detail , name='product_detail'), 
    path('menu_detail/',menu_detail , name='menu_detail'), 

    path('add_product_category/', add_product_category,name='add_product_category'), 
    path('edit_product_category/',edit_product_category , name='edit_product_category'), 
    path('product_category_list/', product_category_list,name='product_category_list'),     
    path('save_edit_product_category/',save_edit_product_category , name='save_edit_product_category'), 
    path('delete_product_category/',delete_product_category , name='delete_product_category'), 

    
    path('invoice_list/',invoice_list , name='invoice_list'), 

    path('product_sales/',product_sales , name='product_sales'), 
    path('get_customer/',get_customer , name='get_customer'), 
    path('get_product_name/',get_product_name , name='get_product_name'), 
    path('add_invoice_item_from_cust/<str:customer_code>/',add_invoice_item_from_cust, name='add_invoice_item_from_cust'),
    path('add_invoice_item/',add_invoice_item, name='add_invoice_item'),           
    url(r'^(?P<product_category_slug>[-\w]+)/$',product,name='product_list_by_category'), 
    url(r'^product/product_menu/(?P<product_category_slug>[-\w]+)/$', product_menu, name='product_list_by_category_2'),          
    url(r'^(?P<product_id>\d+)/(?P<slug>[-\w]+)/$',product_detail,name='product_detail'),

    url(r'^checkout/$',views.checkout,name='checkout'),
    #path('checkout/', checkout, name='checkout'),
    path('order_detail', order_detail, name='order_detail'),

    ]


