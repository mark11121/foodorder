from django.shortcuts import render
from .models import *
from .forms import *
from main.form import SearchForm
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404




def photo_gallery(request):
    photos = Photo.objects.all()
    return render(request, 'gallery/gallery.html', {'photos': photos})


def add_photo(request):
    if request.method == 'POST':
        form = PhotoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save() 
            return HttpResponseRedirect('/gallery/add_photo/')
        else:
            items='error'
            return render(request, 'show_test.html', locals()) 
    else:
        form = PhotoForm()
    return render(request, 'gallery/add_photo.html', {'form': form})



def edit_photo(request, pid):
    photo = Photo.objects.get(id=pid)
    photo_categories = Photo_category.objects.all()    

    if request.method == 'POST':
        if len(request.FILES) !=0:
            if photo.image and len(photo.image) > 0:
                os.remove(photo.image.path)
            photo.image = request.FILES['image']

        # Check if delete_image checkbox is selected
        if 'delete_image' in request.POST:
            if len(photo.image) > 0:
                os.remove(photo.image.path)
            photo.image = None

        photo_category = get_object_or_404(Photo_category, id=request.POST.get('photo_category'))
        photo.photo_category = photo_category
        photo.title          = request.POST.get('title')
        photo.description    = request.POST.get('description')
        photo.save()
        return HttpResponseRedirect('/gallery/photo_list/')

    context = {'photo':photo,
               'photo_categories': photo_categories,}
    return render(request,'gallery/edit_photo.html',context)


def delete_photo(request):
    #兩種get取值方法都可以
    pid = request.GET.get('pid')
    #myid = request.GET['myid']
     
    recd = Photo.objects.get(id=pid)
    if recd.image and len(recd.image)>= 0:
       os.remove(recd.image.path)
    recd.delete()
    
    return HttpResponseRedirect('/gallery/photo_list/')


'''
def save_edit_photo(request):
    pid  = request.POST['pid']
    photos = Photo.objects.get(id=pid)
    form = PhotoForm(request.POST,  request.FILES, instance=photos)
    
    if request.method=='POST':
        
        if 'image-clear' in request.POST:
            if photos.image and len(photos.image) >= 0:
               # Remove the image file
               os.remove(photos.image.path)
               photos.image = None
            photos.save()
            redirect_url = '/gallery/edit_photo/?pid='+pid
        
            # Redirect to the constructed URL
            return HttpResponseRedirect(redirect_url)

        if form.is_valid():
            form.save()

            return HttpResponseRedirect('/gallery/photo_list/')
        else:
            items='error'
            return render(request, 'gallery/gallery.html') 
    else:
           return HttpResponseRedirect('/gallery/photo_list/')
'''



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
            search_params = {}
            for field_name in searchform_params['fields']:
                field_value = searchform.cleaned_data.get(field_name)
                if field_name in searchform_params['category_fields']:
                    if field_value:
                        search_params[field_name + '__name__icontains'] = field_value
                else:
                    if field_value:
                        search_params[field_name + '__icontains'] = field_value

            photo_list = Photo.objects.filter(**search_params)
            paginator = Paginator(photo_list, 6)
            photos = paginator.get_page(1)  # start at page 1 when initiating new search
            total_records = paginator.count

    else:
        searchform = SearchForm(
            initial_data=request.GET,
            **searchform_params
        )

    context = {
        'photos': photos,
        'searchform': searchform,
        'total_records':total_records,
        'searchform_params': searchform_params,  # 添加 searchform_params 到上下文
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

            photo_category_list = Photo_category.objects.filter(**search_params)
            paginator = Paginator(photo_category_list, 6)
            photo_categorys = paginator.get_page(1)  # start at page 1 when initiating new search
            total_records = paginator.count

    else:
        searchform = SearchForm(
            initial_data=request.GET,
            **searchform_params
        )

    context = {
        'photo_categorys': photo_categorys,
        'searchform': searchform,
        'total_records':total_records,
        'searchform_params': searchform_params,  # 添加 searchform_params 到上下文
    }

    return render(request, 'gallery/photo_category_list.html',context)


