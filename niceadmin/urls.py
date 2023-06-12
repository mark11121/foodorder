from os import path
from django.urls import path,include, re_path as url
from niceadmin.views import *
   
urlpatterns = [

    path('niceindex',niceindex,name='niceindex'),   
    path('forms_elements/',forms_elements ,name='forms_elements'),   
    path('forms_layouts/',forms_layouts ,name='forms_layouts'),   
    path('forms_validation/',forms_validation ,name='forms_validation'),   
    path('forms_editors/',forms_editors ,name='forms_editors'),   

    path('components_accordion/',components_accordion ,name='components_accordion'),   
    path('components_alerts/',components_alerts ,name='components_alerts'),   
    path('components_badges/',components_badges ,name='components_badges'),   
    path('components_breadcrumbs/',components_breadcrumbs ,name='components_breadcrumbs'),
    path('components_buttons/',components_buttons ,name='components_buttons'),   
    path('components_cards/',components_cards ,name='components_cards'),   
    path('components_carousel/',components_carousel ,name='components_carousel'),   
    path('components_list_group/',components_list_group ,name='components_list_group'),
    path('components_modal/',components_modal ,name='components_modal'),  
    path('components_pagination/',components_pagination ,name='components_pagination'),   
    path('components_progress/',components_progress ,name='components_progress'),   
    path('components_spinner/',components_spinners ,name='components_spinners'),
    path('components_tabs/',components_tabs ,name='components_tabs'),  
    path('components_tooltips/',components_tooltips ,name='components_tooltips'),   
   
    path('tables_data/',tables_data ,name='tables_data'),   
    path('tables_general/',tables_general ,name='tables_general'),   

    path('users_profile/',users_profile ,name='users_profile'),   

    path('icons_bootstrap/',icons_bootstrap ,name='icons_bootstrap'),   
    path('icons_boxicons/',icons_boxicons ,name='icons_boxicons'),   
    path('icons_remix/',icons_remix ,name='icons_remix'),   

    path('pages_faq/',pages_faq ,name='pages_faq'),   
    path('pages_contact/',pages_contact ,name='pages_contact'),   
    path('pages_register/',pages_register ,name='pages_register'),   
    path('pages_login/',pages_login ,name='pages_login'),   
    path('pages_blank/',pages_blank ,name='pages_blank'),   
    path('pages_error_404/',pages_error_404 ,name='pages_error_404'),   
   
    path('charts_apexcharts/',charts_apexcharts ,name='charts_apexcharts'),   
    path('charts_chartjs/',charts_chartjs ,name='charts_chartjs'),   
    path('charts_echarts/',charts_echarts ,name='charts_echarts'),   
    

    
]

