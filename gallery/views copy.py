from django.shortcuts import render
from .models import *
from .forms import *
from main.form import SearchForm
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator




def photo_gallery(request):
    photos = Photo.objects.all()
    return render(request, 'gallery/gallery.html', {'photos': photos})


def add_photo(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = PhotoForm(request.POST, request.FILES)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            form.save() 
            return HttpResponseRedirect('/gallery/add_photo/')
        else:
            items='error'
            return render(request, 'show_test.html', locals()) 
        
    # if a GET (or any other method) we'll create a blank form
    else:
        
        form = PhotoForm()

    return render(request, 'gallery/add_photo.html', {'form': form})



def edit_photo(request):
    # if this is a POST request we need to process the form data
      #兩種get取值方法都可以
    pid  = request.GET.get('pid')
    recd = Photo.objects.get(id=pid)    
    form = PhotoForm(instance=recd)
    return render(request,
                  'gallery/edit_photo.html',
                  {'pid':pid,
                   'form': form})


def delete_photo(request):
    #兩種get取值方法都可以
    pid = request.GET.get('pid')
    #myid = request.GET['myid']
     
    recd = Photo.objects.get(id=pid)
    if recd.image and len(recd.image)>= 0:
       os.remove(recd.image.path)
    recd.delete()
    
    return HttpResponseRedirect('/gallery/photo_list/')


def save_edit_photo(request):
   pid  = request.POST['pid']
   photos = Photo.objects.get(id=pid)
   form = PhotoForm(request.POST,  request.FILES, instance=photos)
    
   if request.method=='POST':
       if form.is_valid():
            form.save()

            return HttpResponseRedirect('/gallery/photo_list/')
       else:
            items='error'
            return render(request, 'gallery/gallery.html') 
   else:
           return HttpResponseRedirect('/gallery/photo_list/')




#category

def add_photo_category(request):
    # if this is a POST request we need to process the form data
    photo_categorys = Photo_category.objects.all()
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = PhotoCategoryForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            form.save()
            # redirect to a new URL:
            return HttpResponseRedirect('/gallery/photo_category_list/')

        else:
            return HttpResponseRedirect('/gallery/add_photo_category/')
    # if a GET (or any other method) we'll create a blank form
    else:
        form = PhotoCategoryForm()
    
    return render(request, 'gallery/add_photo_category.html', {'form': form,'photo_categorys':photo_categorys})



def edit_photo_category(request):
    # if this is a POST request we need to process the form data
      #兩種get取值方法都可以
    pid  = request.GET.get('pid')
    recd = Photo_category.objects.get(id=pid)    
    form = PhotoCategoryForm(instance=recd)
   
    return render(request,
                  'gallery/edit_photo_category.html',
                  {'pid':pid,
                   'form': form})


def save_edit_photo_category(request):
   pid  = request.POST['pid']
   recd = Photo_category.objects.get(id=pid)   
   form = PhotoCategoryForm(request.POST,  request.FILES, instance=recd)
   
   if request.method=='POST':
       if form.is_valid():
            form.save()
            recd = Photo_category.objects.get(id=pid)
            #photo_item_category_id = recd.photo_category_id
            #category_recd=photo_category.objects.get(id=photo_item_category_id)
           
            # redirect to the detail page of the `Band` we just updated

            return HttpResponseRedirect('/gallery/photo_category_list/')

       else:
            items='error'
            return render(request, 'show_test.html', locals()) 
   else:
        return HttpResponseRedirect('/gallery/add_photo_category/')
   

def delete_photo_category(request):
    #兩種get取值方法都可以
    pid = request.GET.get('pid')
    #myid = request.GET['myid']
     
    recd = Photo_category.objects.get(id=pid)

    recd.delete()
    
    return HttpResponseRedirect('/gallery/photo_category_list/')


   

# First searchform is defined inside the POST block with data=request.POST.
# Second searchform is defined inside the same POST block after the search has been done with initial_data=request.GET.
# Third searchform is defined outside of the POST block with initial_data=request.GET.
# Each searchform definition is used for a different purpose:

# The first searchform is used to process the POST data and validate it.
# The second searchform is used to generate a new search form with the original search query data.
# The third searchform is used to generate the initial search form with the initial GET data.

def photo_list(request):
    photo_list = Photo.objects.all()
    paginator = Paginator(photo_list, 6)  # 6 rows per page
    page = request.GET.get('page')
    photos = paginator.get_page(page)
    total_records = paginator.count

    

    searchform_params = {
        'model': Photo,
        'fields': ['photo_category', 'title', 'description'],
        'label_suffixes': {
            'photo_category': '類別',
            'title': '標題',
            'description': '說明',

        }
        ,'category_fields': ['photo_category'],  # 傳遞相應的類別欄位
    }

    if request.method == 'POST':
        searchform = SearchForm(
            data=request.POST,
            **searchform_params
        )

        if searchform.is_valid():
            photo_list = searchform.search()
            paginator = Paginator(photo_list, 6)
            photos = paginator.get_page(1)  # start at page 1 when initiating new search
            total_records = paginator.count

        searchform = SearchForm(
            initial_data=request.GET,
            **searchform_params
        )

    else:
        searchform = SearchForm(
            initial_data=request.GET,
            **searchform_params
        )

    context = {
        'photos': photos,
        'searchform': searchform,
        'total_records':total_records,
    }


    return render(request, 'gallery/photo_list.html', context)



def photo_category_list(request):

    photo_category_list = Photo_category.objects.all()
    paginator = Paginator(photo_category_list, 6)  # 6 rows per page
    page = request.GET.get('page')
    photo_categorys = paginator.get_page(page)
    total_records = paginator.count


    searchform_params = {
        'model': Photo_category,
        'fields': ['name'],
        'label_suffixes': {
            'name': '類別',
        }
        #,'category_fields': ['name'],  # 傳遞相應的類別欄位
    }

    if request.method == 'POST':
        searchform = SearchForm(
            data=request.POST,
            **searchform_params
        )

        if searchform.is_valid():
            photo_category_list = searchform.search()
            paginator = Paginator(photo_category_list, 6)
            photo_categorys = paginator.get_page(1)  # start at page 1 when initiating new search
            total_records = paginator.count

        searchform = SearchForm(
            initial_data=request.GET,
            **searchform_params
        )

    else:
        searchform = SearchForm(
            initial_data=request.GET,
            **searchform_params
        )

    context = {
        'photo_categorys': photo_categorys,
        'searchform': searchform,
        'total_records':total_records,
    }

    return render(request, 'gallery/photo_category_list.html',context)


