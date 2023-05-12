import os
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from blog.models import Blog_category,Blog_item,Comment_item
from blog.form import BlogForm,BlogCategoryForm,CommentForm
from django.shortcuts import render
from django.core.paginator import Paginator

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

def post_blog(request):
     
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = BlogForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            form.save()
            # redirect to a new URL:
            return render(request, 'blog/blog.html')

        else:
            return HttpResponseRedirect('post_blog/')
        
    # if a GET (or any other method) we'll create a blank form
    else:
        form = BlogForm()
    
    return render(request, 'blog/post_blog.html', {'form': form})

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

def save_blog(request):
   
   form = BlogForm(request.POST,  request.FILES)
   
   if request.method=='POST':
       if form.is_valid():
            form.save()
            # redirect to the detail page of the `Band` we just updated
            return HttpResponseRedirect('/blog/blog')
       else:
            items='error'
            return render(request, 'show_test.html', locals()) 
   else:
        return HttpResponseRedirect('/blog/blog')

def edit_blog(request):
    # if this is a POST request we need to process the form data
      #兩種get取值方法都可以
    pid  = request.GET.get('pid')
    recd = Blog_item.objects.get(id=pid)    
    form = BlogForm(instance=recd)
    return render(request,
                  'blog/edit_blog.html',
                  {'pid':pid,
                   'form': form})

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


def del_blog(request):
    #兩種get取值方法都可以
    pid = request.GET.get('pid')
    #myid = request.GET['myid']
     
    res = Blog_item.objects.get(id=pid)
    if res.image and len(res.image)>= 0:
       os.remove(res.image.path)
    res.delete()
    
    return HttpResponseRedirect('/blog/blog')

def del_blog_category(request):
    #兩種get取值方法都可以
    pid = request.GET.get('pid')
    #myid = request.GET['myid']
     
    res = Blog_category.objects.get(id=pid)
    
    res.delete()
    
    return HttpResponseRedirect('/blog/add_blog_category')

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
     
    blogitem = Blog_item.objects.get(id=pid)
    
    blogitem.likes()
     
    return HttpResponseRedirect(ret_addr)

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

