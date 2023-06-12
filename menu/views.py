import os
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from menu.models import Menu_category,Menu_item,Comment_item
from menu.form import MenuForm,MenuCategoryForm,CommentForm
from django.shortcuts import render
from django.core.paginator import Paginator
from main.form import SearchForm

# Create your views here.




def menu(request, menu_category_slug=None):
     
    item_per_page=6
    menu_category = None
    menu_categories = Menu_category.objects.all()
    menu_items  = Menu_item.objects.all()
    comments    = Comment_item.objects.all()

    # 分页，每页6篇文章

    if menu_category_slug:
        menu_category = get_object_or_404(Menu_category, slug=menu_category_slug)
        menu_items = menu_items.filter(menu_category=menu_category)

    paginator = Paginator(menu_items,item_per_page)
    page_number = request.GET.get('page')
    menu_items = paginator.get_page(page_number)        
        
    return render(request,
                  'menu/menu.html',
                  {'menu_category': menu_category,
                   'menu_categories': menu_categories,
                   'menu_items': menu_items,                   
                   'comments':comments,})


def add_menu_item(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = MenuForm(request.POST, request.FILES)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
             
            form.save()
          
            return HttpResponseRedirect('/menu/add_menu_item/')
        else:
            items='error'
            return render(request, 'show_test.html', locals()) 
        
    # if a GET (or any other method) we'll create a blank form
    else:
        
        form = MenuForm()

    return render(request, 'menu/add_menu_item.html', {'form': form})


def edit_menu(request, pid):
    menu = Menu_item.objects.get(id=pid)
    menu_categories = Menu_category.objects.all()    

    if request.method == 'POST':
        if len(request.FILES) !=0:
            if menu.image and len(menu.image) > 0:
                os.remove(menu.image.path)
            menu.image = request.FILES['image']

        # Check if delete_image checkbox is selected
        if 'delete_image' in request.POST:
            if len(menu.image) > 0:
                os.remove(menu.image.path)
            menu.image = None

        menu_category = get_object_or_404(Menu_category, id=request.POST.get('menu_category'))
        menu.menu_category = menu_category
        menu.menu_title          = request.POST.get('menu_title')
        menu.menu_description    = request.POST.get('menu_description')
        menu.price               = request.POST.get('price')
        menu.save()
        return HttpResponseRedirect('/menu/menu_list/')

    context = {'menu':menu,
               'menu_categories': menu_categories,}
    return render(request,'menu/edit_menu.html',context)


def del_menu(request):
    #兩種get取值方法都可以
    pid = request.GET.get('pid')
    #myid = request.GET['myid']
     
    res = Menu_item.objects.get(id=pid)
    if res.image and len(res.image)>= 0:
       os.remove(res.image.path)
    res.delete()
    
    return HttpResponseRedirect('/menu/menu_list')

def save_edit_menu(request):
   pid  = request.POST['pid']
   recd = Menu_item.objects.get(id=pid)
   form = MenuForm(request.POST,  request.FILES, instance=recd)
   
   if request.method=='POST':
       if form.is_valid():
            form.save()
            recd = Menu_item.objects.get(id=pid)
            #menu_item_category_id = recd.menu_category_id
            #category_recd=menu_category.objects.get(id=menu_item_category_id)
            category_slug=recd.slug()
            # redirect to the detail page of the `Band` we just updated
            return HttpResponseRedirect('/menu/'+category_slug)
       
       else:
            items='error'
            return render(request, 'show_test.html', locals()) 
   else:
        return HttpResponseRedirect('/menu/'+category_slug)


def menu_detail(request):
   
    pid = request.GET.get('pid')
    #myid = request.GET['myid']
     
    menu_item = Menu_item.objects.get(id=pid)
    
    return render(request, 'menu/menu-details.html', {
                                                    'menu_item': menu_item ,
                                                     })





#category

def add_menu_category(request):
    # if this is a POST request we need to process the form data
    menu_categorys = Menu_category.objects.all()
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = MenuCategoryForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            form.save()
            # redirect to a new URL:
            return HttpResponseRedirect('/menu/menu_category_list')

        else:
            return HttpResponseRedirect('/menu/add_menu_category/')
    # if a GET (or any other method) we'll create a blank form
    else:
        form = MenuCategoryForm()
    
    return render(request, 'menu/add_menu_category.html', {'form': form,'menu_categorys':menu_categorys})


def edit_menu_category(request):
    # if this is a POST request we need to process the form data
      #兩種get取值方法都可以
    pid  = request.GET.get('pid')
    recd = Menu_category.objects.get(id=pid)    
    form = MenuCategoryForm(instance=recd)
   
    return render(request,
                  'menu/edit_menu_category.html',
                  {'pid':pid,
                   'form': form})


def save_edit_menu_category(request):
   pid  = request.POST['pid']
   recd = Menu_category.objects.get(id=pid)   
   form = MenuCategoryForm(request.POST,  request.FILES, instance=recd)
   category_slug=recd.slug
   
   if request.method=='POST':
       if form.is_valid():
            form.save()
            recd = Menu_category.objects.get(id=pid)
            #menu_item_category_id = recd.menu_category_id
            #category_recd=menu_category.objects.get(id=menu_item_category_id)
           
            # redirect to the detail page of the `Band` we just updated
            return HttpResponseRedirect('/menu/menu_category_list')
       
       else:
            items='error'
            return render(request, 'show_test.html', locals()) 
   else:
        return HttpResponseRedirect('/menu/add_menu_category/')


def del_menu_category(request):
    #兩種get取值方法都可以
    pid = request.GET.get('pid')
    #myid = request.GET['myid']
     
    res = Menu_category.objects.get(id=pid)
    
    res.delete()
    
    return HttpResponseRedirect('/menu/menu_category_list')



# First searchform is defined inside the POST block with data=request.POST.
# Second searchform is defined inside the same POST block after the search has been done with initial_data=request.GET.
# Third searchform is defined outside of the POST block with initial_data=request.GET.
# Each searchform definition is used for a different purpose:

# The first searchform is used to process the POST data and validate it.
# The second searchform is used to generate a new search form with the original search query data.
# The third searchform is used to generate the initial search form with the initial GET data.

def menu_list(request):
    menu_list = Menu_item.objects.all()
    paginator = Paginator(menu_list, 6)  # 6 rows per page
    page = request.GET.get('page')
    menu_items = paginator.get_page(page)
    total_records = paginator.count

    

    searchform_params = {
        'model': Menu_item,
        'fields': ['menu_category', 'menu_title', 'menu_description','price','menu_created_user','menu_created'],
        'label_suffixes': {
            'menu_category': '類別',
            'menu_title': '標題',
            'menu_description': '說明',
            'price': '價格',
            'menu_created_user': '建立者',
            'menu_created': '建立時間',

        }
        ,'category_fields': ['menu_category'],  # 傳遞相應的類別欄位
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

            menu_list = Menu_item.objects.filter(**search_params)
            paginator = Paginator(menu_list, 6)
            menu_items = paginator.get_page(1)  # start at page 1 when initiating new search
            total_records = paginator.count

    else:
        searchform = SearchForm(
            initial_data=request.GET,
            **searchform_params
        )

    context = {
        'menu_items': menu_items,
        'searchform': searchform,
        'total_records':total_records,
        'searchform_params': searchform_params,  # 添加 searchform_params 到上下文
    }


    return render(request, 'menu/menu_list.html', context)



def menu_category_list(request):

    menu_category_list = Menu_category.objects.all()
    paginator = Paginator(menu_category_list, 6)  # 6 rows per page
    page = request.GET.get('page')
    menu_categorys = paginator.get_page(page)
    total_records = paginator.count


    searchform_params = {
        'model': Menu_category,
        'fields': ['name'],
        'label_suffixes': {
            'name': '類別',
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

            menu_category_list = Menu_category.objects.filter(**search_params)
            paginator = Paginator(menu_category_list, 6)
            menu_categorys = paginator.get_page(1)  # start at page 1 when initiating new search
            total_records = paginator.count

    else:
        searchform = SearchForm(
            initial_data=request.GET,
            **searchform_params
        )

    context = {
        'menu_categorys': menu_categorys,
        'searchform': searchform,
        'total_records':total_records,
        'searchform_params': searchform_params,  # 添加 searchform_params 到上下文
    }

    return render(request, 'menu/menu_category_list.html',context)














def post_comment(request):
     
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
 
        myname = request.POST['name']
        myemail = request.POST['email']
        mywebsite = request.POST['website']
        mycomment = request.POST['comment']
        mybid = request.POST['bid']
        ret_addr = request.POST['ret_addr']
        

        recd = Comment_item.objects.create(bid=mybid,menu_item_id=mybid,name=myname,email=myemail,website=mywebsite,comment=mycomment)        
        recd.save()
        recd = Comment_item.objects.filter(menu_item_id=mybid)   

    return HttpResponseRedirect(ret_addr)


def del_comment(request,):
    #兩種get取值方法都可以
    pid = request.GET.get('pid')
    ret_addr= request.GET.get('ret_addr')
    #myid = request.GET['myid']
     
    res = Comment_item.objects.get(id=pid)
    
    res.delete()
     
    return HttpResponseRedirect(ret_addr)

def press_like(request,):
    
    pid = request.GET.get('pid')
    ret_addr= request.GET.get('ret_addr')
    #myid = request.GET['myid']
     
    menuitem = Menu_item.objects.get(id=pid)
    
    menuitem.likes()
     
    return HttpResponseRedirect(ret_addr)



def search_title(request):
    q_title = request.POST['q_title']
    category = None
    categories = Menu_category.objects.all()
    menuitems  = Menu_item.objects.filter(menu_title__icontains=q_title)
    

    comments   = Comment_item.objects.all()

    return render(request,
                  'menu/menu.html',
                  {'category': category,
                   'categories': categories,
                   'menuitems': menuitems,                   
                   'comments':comments,})
