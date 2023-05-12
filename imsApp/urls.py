from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static
from . import views
from django.contrib.auth import views as auth_views
from django.views.generic.base import RedirectView

urlpatterns = [
    path('home',views.home,name='home-page'),
    path('profile',views.profile,name='profile'),
    path('update-profile',views.update_profile,name='update-profile'),
    path('update-password',views.update_password,name='update-password'),
    path('category',views.category_mgt,name='category-page'),
    path('manage_category',views.manage_category,name='manage-category'),
    path('save_category',views.save_category,name='save-category'),
    path('manage_category/<int:pk>',views.manage_category,name='manage-category-pk'),
    path('delete_category',views.delete_category,name='delete-category'),
    path('product',views.product_mgt,name='product-page'),
    path('manage_product',views.manage_product,name='manage-product'),
    path('save_product',views.save_product,name='save-product'),
    path('manage_product/<int:pk>',views.manage_product,name='manage-product-pk'),
    path('delete_product',views.delete_product,name='delete-product'),
    path('inventory',views.inventory,name='inventory-page'),
    path('inventory/<int:pk>',views.inv_history,name='inventory-history-page'),
    path('stock/<int:pid>',views.manage_stock,name='manage-stock'),
    path('stock/<int:pid>/<int:pk>',views.manage_stock,name='manage-stock-pk'),
    path('save_stock',views.save_stock,name='save-stock'),
    path('delete_stock',views.delete_stock,name='delete-stock'),
    path('sales',views.sales_mgt,name='sales-page'),
    path('get_product',views.get_product,name='get-product'),
    path('get_product/<int:pk>',views.get_product),
    path('save_sales',views.save_sales, name="save-sales"),
    path('invoices',views.invoices,name='invoice-page'),
    path('delete_invoice',views.delete_invoice,name='delete-invoice'),
    path('accounts/', include(('accounts.urls', 'accounts'), namespace='accounts')),
    
]
