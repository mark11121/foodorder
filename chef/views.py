import os
from django.shortcuts import render
from .models import *
from .form import *
from django.views.generic import *
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator
from main.form import SearchForm
# Create your views here.

def chef(request):
    chefs = Chef.objects.all()
    delay_count = 100
    for i, chef in enumerate(chefs):
        chef.delay = delay_count
        delay_count += 100
    return render(request, 
                  'chef/chefs.html', 
                  {'chefs': chefs})

def add_chef(request):
    if request.method == 'POST':
        form = ChefForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/chef/chef/')
        else:
            items='error'
            return render(request, 'show_test.html', locals()) 
    else:
        form = ChefForm()
    return render(request, 'chef/add_chef.html', {'form': form})


def edit_chef(request, pid):
    chef = Chef.objects.get(id=pid)

    if request.method == 'POST':
        if len(request.FILES) !=0:
            if chef.chef_img and len(chef.chef_img) > 0:
                os.remove(chef.chef_img.path)
            chef.chef_img = request.FILES['chef_img']

        # Check if delete_image checkbox is selected
        if 'delete_image' in request.POST:
            if len(chef.chef_img) > 0:
                os.remove(chef.chef_img.path)
            chef.chef_img = None

        chef.chef_name      = request.POST.get('chef_name')
        chef.chef_title     = request.POST.get('chef_title')
        chef.chef_profile   = request.POST.get('chef_profile')
        chef.save()
        return HttpResponseRedirect('/chef/chef_list/')

    context = {'chef':chef}
    return render(request,'chef/edit_chef.html',context)


def delete_chef(request):
    #兩種get取值方法都可以
    pid = request.GET.get('pid')
    #myid = request.GET['myid']
     
    res = Chef.objects.get(id=pid)
    if res.chef_img and len(res.chef_img)>= 0:
       os.remove(res.chef_img.path)
    res.delete()
    
    return HttpResponseRedirect('/chef/chef')

'''
def save_edit_chef(request):
   pid=request.POST['pid']
   recd = Chef.objects.get(id=pid)
   form = ChefForm(request.POST,  request.FILES, instance=recd)
   
   if request.method=='POST':
       if form.is_valid():
            form.save()
            recd = Chef.objects.get(id=pid)
            #blog_item_category_id = recd.blog_category_id
            #category_recd=Blog_category.objects.get(id=blog_item_category_id)
            #category_slug=recd.slug()
            # redirect to the detail page of the `Band` we just updated
            return HttpResponseRedirect('/chef/chef')
       
       else:
            items='error'
            return render(request, 'chef/chefs.html') 
   else:
        return HttpResponseRedirect('/chef/chef')
'''

# First searchform is defined inside the POST block with data=request.POST.
# Second searchform is defined inside the same POST block after the search has been done with initial_data=request.GET.
# Third searchform is defined outside of the POST block with initial_data=request.GET.
# Each searchform definition is used for a different purpose:

# The first searchform is used to process the POST data and validate it.
# The second searchform is used to generate a new search form with the original search query data.
# The third searchform is used to generate the initial search form with the initial GET data.

def chef_list(request):
    chef_list = Chef.objects.all()
    paginator = Paginator(chef_list, 6)  # 6 rows per page
    page = request.GET.get('page')
    chefs = paginator.get_page(page)
    total_records = paginator.count

    searchform_params = {
        'model': Chef,
        'fields': ['chef_name', 'chef_title', 'chef_profile'],
        'label_suffixes': {
            'chef_name': '廚師名稱',
            'chef_title': '廚師頭銜',
            'chef_profile': '廚師介紹',

        }
        ,'category_fields': []  # 添加空列表作为类别字段
    }

    if request.method == 'POST':
        searchform = SearchForm(
            data=request.POST,
            **searchform_params
        )

        if searchform.is_valid():
            search_params = {}
            for field_name in searchform_params['fields']:
                field_value = searchform.cleaned_data.get(field_name)
                if field_name in searchform_params['category_fields']:
                    if field_value:
                        search_params[field_name + '__name__icontains'] = field_value
                else:
                    if field_value:
                        search_params[field_name + '__icontains'] = field_value

            chef_list = Chef.objects.filter(**search_params)
            paginator = Paginator(chef_list, 6)
            chefs = paginator.get_page(1)  # start at page 1 when initiating new search
            total_records = paginator.count

    else:
        searchform = SearchForm(
            initial_data=request.GET,
            **searchform_params
        )

    context = {
        'chefs': chefs,
        'searchform': searchform,
        'total_records':total_records,
        'searchform_params': searchform_params,  # 添加 searchform_params 到上下文
    }

    return render(request, 'chef/chef_list.html', context)
