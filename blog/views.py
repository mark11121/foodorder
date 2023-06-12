import os
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from blog.models import Blog_category,Blog_item,Comment_item
from blog.form import BlogForm,BlogCategoryForm,CommentForm
from django.shortcuts import render
from django.core.paginator import Paginator
from main.form import SearchForm

# Create your views here.


def blog(request, category_slug=None):

    item_per_page=6
    category = None
    categories = Blog_category.objects.all()
    blogitems  = Blog_item.objects.all()
    comments   = Comment_item.objects.all()

    # 分页，每页6篇文章

    if category_slug:
        category = get_object_or_404(Blog_category, slug=category_slug)
        blogitems = blogitems.filter(blog_category=category)

    paginator = Paginator(blogitems,item_per_page)
    page_number = request.GET.get('page')
    blogitems = paginator.get_page(page_number)        
        
    return render(request,
                  'blog/blog.html',
                  {'category': category,
                   'categories': categories,
                   'blogitems': blogitems,                   
                   'comments':comments,})


def add_blog(request):
     
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = BlogForm(request.POST, request.FILES)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            form.save()
            # redirect to a new URL:
            return HttpResponseRedirect('/blog/blog')

        else:
            return HttpResponseRedirect('add_blog/')
        
    # if a GET (or any other method) we'll create a blank form
    else:
        form = BlogForm()
    
    return render(request, 'blog/add_blog.html', {'form': form})


def edit_blog(request, pid):
    blog = Blog_item.objects.get(id=pid)
    blog_categories = Blog_category.objects.all()    

    if request.method == 'POST':
        if len(request.FILES) !=0:
            if blog.image and len(blog.image) > 0:
                os.remove(blog.image.path)
            blog.image = request.FILES['image']

        # Check if delete_image checkbox is selected
        if 'delete_image' in request.POST:
            if len(blog.image) > 0:
                os.remove(blog.image.path)
            blog.image = None

        blog_category = get_object_or_404(Blog_category, id=request.POST.get('blog_category'))
        blog.blog_category = blog_category
        blog.blog_title    = request.POST.get('blog_title')
        blog.blog_content  = request.POST.get('blog_content')
        blog.blog_user     = request.POST.get('blog_user')
        blog.save()
        return HttpResponseRedirect('/blog/blog_list/')

    context = {'blog':blog,
               'blog_categories': blog_categories,}
    return render(request,'blog/edit_blog.html',context)


def delete_blog(request):
    #兩種get取值方法都可以
    pid = request.GET.get('pid')
    #myid = request.GET['myid']
     
    res = Blog_item.objects.get(id=pid)
    if res.image and len(res.image)>= 0:
       os.remove(res.image.path)
    res.delete()
    
    return HttpResponseRedirect('/blog/blog')

'''
def save_edit_blog(request):
   pid=request.POST['pid']
   recd = Blog_item.objects.get(id=pid)
   form = BlogForm(request.POST,  request.FILES, instance=recd)
   
   if request.method=='POST':
       if form.is_valid():
            form.save()
            recd = Blog_item.objects.get(id=pid)
            #blog_item_category_id = recd.blog_category_id
            #category_recd=Blog_category.objects.get(id=blog_item_category_id)
            category_slug=recd.slug()
            # redirect to the detail page of the `Band` we just updated
            return HttpResponseRedirect('/blog/'+category_slug)
       
       else:
            items='error'
            return render(request, 'show_test.html', locals()) 
   else:
        return HttpResponseRedirect('/blog/'+category_slug)
'''


def blog_detail(request):
   
    categories = Blog_category.objects.all()

    pid = request.GET.get('pid')
    #myid = request.GET['myid']
     
    res = Blog_item.objects.get(id=pid)
    category = res.blog_category
    cres = Comment_item.objects.filter(bid=pid)

    blogitems   = Blog_item.objects.filter(blog_category=category)

    return render(request, 'blog/blog-details.html', {'res':res ,
                                                      'cres':cres,
                                                      'categories':categories,
                                                      'blogitems':blogitems,
                                                     })





#category


def add_blog_category(request):
    # if this is a POST request we need to process the form data
    blog_categorys = Blog_category.objects.all()
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = BlogCategoryForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            form.save()
            # redirect to a new URL:
            return HttpResponseRedirect('/blog/blog/')

        else:
            return HttpResponseRedirect('/blog/add_blog_category/')
    # if a GET (or any other method) we'll create a blank form
    else:
        form = BlogCategoryForm()
    
    return render(request, 'blog/add_blog_category.html', {'form': form,'blog_categorys':blog_categorys})


def edit_blog_category(request):
    # if this is a POST request we need to process the form data
      #兩種get取值方法都可以
    pid  = request.GET.get('pid')
    recd = Blog_category.objects.get(id=pid)    
    form = BlogCategoryForm(instance=recd)
   
    return render(request,
                  'blog/edit_blog_category.html',
                  {'pid':pid,
                   'form': form})

def save_edit_blog_category(request):
   pid  = request.POST['pid']
   recd = Blog_category.objects.get(id=pid)   
   form = BlogCategoryForm(request.POST,  request.FILES, instance=recd)
   category_slug=recd.slug
   
   if request.method=='POST':
       if form.is_valid():
            form.save()
            recd = Blog_category.objects.get(id=pid)
            #blog_item_category_id = recd.blog_category_id
            #category_recd=Blog_category.objects.get(id=blog_item_category_id)
           
            # redirect to the detail page of the `Band` we just updated
            return HttpResponseRedirect('/blog/'+category_slug)
       
       else:
            items='error'
            return render(request, 'show_test.html', locals()) 
   else:
        return HttpResponseRedirect('/blog/'+category_slug)


def delete_blog_category(request):
    #兩種get取值方法都可以
    pid = request.GET.get('pid')
    #myid = request.GET['myid']
     
    res = Blog_category.objects.get(id=pid)
    
    res.delete()
    
    return HttpResponseRedirect('/blog/add_blog_category')



#留言comment

def post_comment(request):
     
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
 
        myname = request.POST['name']
        myemail = request.POST['email']
        mywebsite = request.POST['website']
        mycomment = request.POST['comment']
        mybid = request.POST['bid']
        ret_addr = request.POST['ret_addr']
        

        recd = Comment_item.objects.create(bid=mybid,blog_item_id=mybid,name=myname,email=myemail,website=mywebsite,comment=mycomment)        
        recd.save()
        recd = Comment_item.objects.filter(blog_item_id=mybid)   

    return HttpResponseRedirect(ret_addr)


def del_comment(request,):
    #兩種get取值方法都可以
    pid = request.GET.get('pid')
    ret_addr= request.GET.get('ret_addr')
    #myid = request.GET['myid']
     
    res = Comment_item.objects.get(id=pid)
    
    res.delete()
     
    return HttpResponseRedirect(ret_addr)


#按讚

def press_like(request,):
    
    pid = request.GET.get('pid')
    ret_addr= request.GET.get('ret_addr')
    #myid = request.GET['myid']
     
    blogitem = Blog_item.objects.get(id=pid)
    
    blogitem.likes()
     
    return HttpResponseRedirect(ret_addr)


#倒讚

def press_hate(request,):
    
    pid = request.GET.get('pid')
    ret_addr= request.GET.get('ret_addr')
    #myid = request.GET['myid']
     
    blogitem = Blog_item.objects.get(id=pid)
    
    blogitem.hates()
     
    return HttpResponseRedirect(ret_addr)


#搜尋

def search_title(request):
    q_title = request.POST['q_title']
    category = None
    categories = Blog_category.objects.all()
    blogitems  = Blog_item.objects.filter(blog_title__icontains=q_title)
    

    comments   = Comment_item.objects.all()

    return render(request,
                  'blog/blog.html',
                  {'category': category,
                   'categories': categories,
                   'blogitems': blogitems,                   
                   'comments':comments,})



# First searchform is defined inside the POST block with data=request.POST.
# Second searchform is defined inside the same POST block after the search has been done with initial_data=request.GET.
# Third searchform is defined outside of the POST block with initial_data=request.GET.
# Each searchform definition is used for a different purpose:

# The first searchform is used to process the POST data and validate it.
# The second searchform is used to generate a new search form with the original search query data.
# The third searchform is used to generate the initial search form with the initial GET data.

def blog_list(request):
    blog_list = Blog_item.objects.all()
    paginator = Paginator(blog_list, 6)  # 6 rows per page
    page = request.GET.get('page')
    blogs = paginator.get_page(page)
    total_records = paginator.count

    

    searchform_params = {
        'model': Blog_item,
        'fields': ['blog_category', 'blog_title', 'blog_content','blog_user','blog_created'],
        'label_suffixes': {
            'blog_category': '類別',
            'blog_title': '標題',
            'blog_content': '內文',
            'blog_user':'作者',
            'blog_created':'發文時間',

        }
        ,'category_fields': ['blog_category'],  # 傳遞相應的類別欄位
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

            blog_list = Blog_item.objects.filter(**search_params)
            paginator = Paginator(blog_list, 6)
            blogs = paginator.get_page(1)  # start at page 1 when initiating new search
            total_records = paginator.count

    else:
        searchform = SearchForm(
            initial_data=request.GET,
            **searchform_params
        )

    context = {
        'blogs': blogs,
        'searchform': searchform,
        'total_records':total_records,
        'searchform_params': searchform_params,  # 添加 searchform_params 到上下文
    }


    return render(request, 'blog/blog_list.html', context)



def blog_category_list(request):

    blog_category_list = Blog_category.objects.all()
    paginator = Paginator(blog_category_list, 6)  # 6 rows per page
    page = request.GET.get('page')
    blog_categorys = paginator.get_page(page)
    total_records = paginator.count


    searchform_params = {
        'model': Blog_category,
        'fields': ['name'],
        'label_suffixes': {
            'name': '類別名稱',
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

            blog_category_list = Blog_category.objects.filter(**search_params)
            paginator = Paginator(blog_category_list, 6)
            blog_categorys = paginator.get_page(1)  # start at page 1 when initiating new search
            total_records = paginator.count

    else:
        searchform = SearchForm(
            initial_data=request.GET,
            **searchform_params
        )

    context = {
        'blog_categorys': blog_categorys,
        'searchform': searchform,
        'total_records':total_records,
        'searchform_params': searchform_params,  # 添加 searchform_params 到上下文
    }

    return render(request, 'blog/blog_category_list.html',context)


