"""nova URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from os import path
from django.conf import settings
from django.urls import path,include, re_path as url
from django.conf.urls.static import static
from django.contrib import admin
from django_select2 import urls as select2_urls


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(('main.urls', 'main'), namespace='main')),
    path('accounts/', include(('accounts.urls', 'accounts'), namespace='accounts')),
    path('blog/', include(('blog.urls', 'blog'), namespace='blog')), 
    path('menu/', include(('menu.urls', 'menu'), namespace='menu')),     
    path('product/', include(('product.urls', 'product'), namespace='product')),
    path('select2/', include(select2_urls)),
    path('imsApp/', include(('imsApp.urls', 'imsApp'), namespace='imsApp')),    
    path('chef/', include(('chef.urls', 'chef'), namespace='chef')),      
    path('gallery/', include(('gallery.urls', 'gallery'), namespace='photo_gallery')),    
    path('niceadmin/', include(('niceadmin.urls', 'niceadmin'), namespace='niceadmin')),                   
    #url(r'^orders/', include(('orders.urls', 'orders'), namespace='orders')),
    #url(r'^payment/', include(('payment.urls', 'payment'), namespace='payment')),
    #url(r'^paypal/', include('paypal.standard.ipn.urls')),
    path('cart/', include(('cart.urls', 'cart'), namespace='cart')),   

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)

