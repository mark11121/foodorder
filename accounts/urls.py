from django.urls import path
from accounts.views import *

app_name = 'accounts'

urlpatterns = [
    path('signup/', signup_view, name="signup"),
    path('signup_new/', signup_new_view, name="signup_new"),
    path('login/', login_view, name="login"),
    path('logout/', logout_view, name="logout"),
    path('user_list/', user_list, name='user_list'),
    path('make_superuser/<int:user_id>/', make_superuser, name='make_superuser'),
    path('del_superuser/<int:user_id>/', del_superuser, name='del_superuser'),
    path('del_user/<int:user_id>/', del_user, name='del_user'),
    path('edit_profile/<int:user_id>/', edit_profile, name='edit_profile'),
    path('add_profile/<int:user_id>/',add_profile, name='add_profile'),
    path('save_edit_profile/',save_edit_profile, name='save_edit_profile'),
    path('del_profile/<int:user_id>/',del_profile, name='del_profile'),
    path('create_customer/', create_customer, name='create_customer'),
    path('customer_detail/', customer_detail, name='customer_detail'),
    path('customer_list/', customer_list, name='customer_list'),
]

