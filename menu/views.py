import os
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from menu.models import Menu_category,Menu_item,Comment_item
from menu.form import MenuForm,MenuCategoryForm,CommentForm
from django.shortcuts import render
from django.core.paginator import Paginator

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

def edit_menu(request):
    # if this is a POST request we need to process the form data
      #兩種get取值方法都可以
    pid  = request.GET.get('pid')
    recd = Menu_item.objects.get(id=pid)    
    form = MenuForm(instance=recd)
    return render(request,
                  'menu/edit_menu.html',
                  {'pid':pid,
                   'form': form})


def del_menu(request):
    #兩種get取值方法都可以
    pid = request.GET.get('pid')
    #myid = request.GET['myid']
     
    res = Menu_item.objects.get(id=pid)
    if res.image and len(res.image)>= 0:
       os.remove(res.image.path)
    res.delete()
    
    return HttpResponseRedirect('/menu/menu/')

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
            return HttpResponseRedirect('/menu/menu/')

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
            return HttpResponseRedirect('/menu/add_menu_category/')
       
       else:
            items='error'
            return render(request, 'show_test.html', locals()) 
   else:
        return HttpResponseRedirect('/menu/add_menu_category/')












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

def save_menu(request):
   
   form = MenuForm(request.POST,  request.FILES)
   
   if request.method=='POST':
       if form.is_valid():
            form.save()
            # redirect to the detail page of the `Band` we just updated
            return HttpResponseRedirect('/menu/menu')
       else:
            items='error'
            return render(request, 'show_test.html', locals()) 
   else:
        return HttpResponseRedirect('/menu/menu')


def del_menu_category(request):
    #兩種get取值方法都可以
    pid = request.GET.get('pid')
    #myid = request.GET['myid']
     
    res = Menu_category.objects.get(id=pid)
    
    res.delete()
    
    return HttpResponseRedirect('/menu/add_menu_category')





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

def menu_detail(request):
   
    pid = request.GET.get('pid')
    #myid = request.GET['myid']
     
    menu_item = Menu_item.objects.get(id=pid)
    
    return render(request, 'menu/menu-details.html', {
                                                    'menu_item': menu_item ,
                                                     })

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
