import os
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from menu.models import *
from blog.models import *
from chef.models import *
from django.core.paginator import Paginator
# Create your views here.


def index(request, category_slug=None):

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
                  'main/index.html',
                  {'category': category,
                   'categories': categories,
                   'blogitems': blogitems,                   
                   'comments':comments,})


def about(request):
    chefs = Chef.objects.all()
    delay_count = 100
    for i, chef in enumerate(chefs):
        chef.delay = delay_count
        delay_count += 100
    return render(request, 
                  'main/about.html', 
                  {'chefs': chefs})



def event(request):
    return render(request,'main/event.html')

def chefs(request):
    return render(request,'main/chefs.html')

def gellery(request):
    return render(request,'main/gellery.html')

def contact(request):
    return render(request,'main/contact.html')

def contact(request):
    return render(request,'main/contact.html')



