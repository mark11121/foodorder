from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from product.models import Product_category,Product,Invoice,Invoice_Item
from product.forms import *
from django.shortcuts import render
from django.core.paginator import Paginator
from django.views.generic import ListView
from .models import Invoice
from main.form import SearchForm

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from accounts.models import Customer

@csrf_exempt
def get_customer(request):
    if request.method == 'POST':
        customer_code = request.POST.get('customer_code', None)
        if customer_code is not None:
            customer = get_object_or_404(Customer, customer_code=customer_code)
            data = {
                'last_name': customer.last_name,
                'first_name': customer.first_name,
            }
            return JsonResponse(data)
        else:
            return JsonResponse({'error': 'Missing customer_code parameter'})
    else:
        return JsonResponse({'error': 'Invalid request method'})

@csrf_exempt
def get_product_name(request):
    if request.method == 'POST':
        product_code = request.POST.get('product_code', None)
        if product_code is not None:
            product = Product.objects.filter(code=product_code).first()
            data = {
                'name': product.name,
                'price': product.price,
            }
            return JsonResponse(data)
        else:
            return JsonResponse({'error': 'Missing product_code parameter'})
    else:
        return JsonResponse({'error': 'Invalid request method'})

class InvoiceListView(ListView):
    model = Invoice
    template_name = 'product/invoice_list.html'
    context_object_name = 'invoices'
    queryset = Invoice.objects.prefetch_related('invoice_item_set')

def product_sales(request):
    invoice_list = Invoice.objects.all()
    paginator = Paginator(invoice_list, 6)  # 6 rows per page
    page = request.GET.get('page')
    invoices = paginator.get_page(page)
    total_records = paginator.count
    searchform_params = {
        'model': Invoice,
        'fields': ['transaction', 'customer', 'total', 'date_created', 'invoice_item__product__name','invoice_item__stock__quantity'],
        'label_suffixes': {
            'transaction': '交易編號',
            'customer': '客戶',
            'total': '總價',
            'date_created': '發票日期 ',
            'invoice_item__product__name': '商品名稱',
            'invoice_item__stock__quantity': '庫存數量',
        }
    }

    if request.method == 'POST':
        searchform = SearchForm(
            data=request.POST,
            **searchform_params
        )

        if searchform.is_valid():
            invoice_list = searchform.search()
            paginator = Paginator(invoice_list, 6)
            invoices = paginator.get_page(1)  # start at page 1 when initiating new search
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
        'invoices': invoices,
        'searchform': searchform,
        'total_records':total_records,
        'forms':Product_Sales_Form,
    }

    return render(request, 'product/invoice_list.html',context)


def product(request, product_category_slug=None):
     
    item_per_page=6
    product_category = None
    product_categories = Product_category.objects.all()
    product_items      = Product.objects.all()
   
    # 分页，每页6篇文章

    if product_category_slug:
        product_category = get_object_or_404(Product_category, slug=product_category_slug)
        product_items = product_items.filter(product_category=product_category)

    paginator = Paginator(product_items,item_per_page)
    page_number = request.GET.get('page')
    product_items = paginator.get_page(page_number)        
        
    return render(request,
                  'product/product.html',
                  {'product_category': product_category,
                   'product_categories': product_categories,
                   'product_items': product_items,                 
                   })


def add_product_category(request):
    # if this is a POST request we need to process the form data
    product_categorys = Product_category.objects.all()
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = ProductCategoryForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            form.save()
            # redirect to a new URL:

            return HttpResponseRedirect('/product/product_category_list/')
        else:
            return HttpResponseRedirect('/product/add_product_category/')
    # if a GET (or any other method) we'll create a blank form
    else:
        form = ProductCategoryForm()
    
    return render(request, 'product/add_product_category.html', {'form': form,'product_categorys':product_categorys})

def edit_product_category(request):
    # if this is a POST request we need to process the form data
      #兩種get取值方法都可以
    pid  = request.GET.get('pid')
    recd = Product_category.objects.get(id=pid)    
    form = ProductCategoryForm(instance=recd)
   
    return render(request,
                  'product/edit_product_category.html',
                  {'pid':pid,
                   'form': form})

def save_edit_product_category(request):
   pid  = request.POST['pid']
   recd = Product_category.objects.get(id=pid)   
   form = ProductCategoryForm(request.POST,  request.FILES, instance=recd)
   
   
   if request.method=='POST':
       if form.is_valid():
            form.save()
            recd = Product_category.objects.get(id=pid)
            #product_item_category_id = recd.product_category_id
            #category_recd=product_category.objects.get(id=product_item_category_id)
           
            # redirect to the detail page of the `Band` we just updated
            product_categorys = Product_category.objects.all()

            return HttpResponseRedirect('/product/product_category_list/')

       else:
            items='error'
            return render(request, 'show_test.html', locals()) 
   else:
        return HttpResponseRedirect('/product/add_product_category/')
   

def delete_product_category(request):
    #兩種get取值方法都可以
    pid = request.GET.get('pid')
    #myid = request.GET['myid']
     
    recd = Product_category.objects.get(id=pid)

    recd.delete()
    
    return HttpResponseRedirect('/product/product_category_list/')

def add_product(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = ProductForm(request.POST, request.FILES)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
             
            form.save()
          
            return HttpResponseRedirect('/product/add_product/')
        else:
            items='error'
            return render(request, 'show_test.html', locals()) 
        
    # if a GET (or any other method) we'll create a blank form
    else:
        
        form = ProductForm()

    return render(request, 'product/add_product.html', {'form': form})


def add_invoice_it2em(request):
    if request.method == 'POST':
        form = Product_Sales_Form(request.POST)
        if form.is_valid():
            customer = form.cleaned_data['customer']
            transaction = form.cleaned_data['transaction']
            product = form.cleaned_data['product']
            quantity = form.cleaned_data['quantity']

            invoice = Invoice.objects.create(transaction=transaction, customer=customer)
            invoice_item = Invoice_Item.objects.create(invoice=invoice, product=product, price=product.price, quantity=quantity)

            return render(request, 'product/invoice_list.html')
    else:
        form = Product_Sales_Form()

    return render(request, 'product/add_invoice_item.html', {'form': form})


def add_invoice_item_from_cust(request, customer_code):

    products=Product.objects.all()

    if request.method == 'POST':
        form = Product_Sales_Form(request.POST)
        if form.is_valid():
           customer_code = form.cleaned_data['customer_code']
           customer = form.cleaned_data['customer']
           transaction = form.cleaned_data['transaction']
           quantity = form.cleaned_data['quantity']
           code     = form.cleaned_data['code']
           price    = form.cleaned_data['quantity']

           invoice = Invoice.objects.create(transaction=transaction, customer_code=customer_code, customer=customer)
           invoice_item = Invoice_Item.objects.create(invoice=invoice, price=price, quantity=quantity)

           return HttpResponseRedirect('/accounts/customer_list/')
    else:
        # Initialize the form with the `customer_code` value
        form = Product_Sales_Form(initial={'customer_code': customer_code})

    context = {
        'form': form,
        'products':products,
    }

    return render(request, 'product/add_invoice_item_from_cust.html', context)

def add_invoice_item(request):
    products=Product.objects.all()

    if request.method == 'POST':
        form = Product_Sales_Form(request.POST)
        
        if form.is_valid():
            customer_code = form.cleaned_data['customer_code']
            customer = form.cleaned_data['customer']
            transaction = form.cleaned_data['transaction']
            quantity = form.cleaned_data['quantity']
            code    = form.cleaned_data['code']
            price    = form.cleaned_data['quantity']

            invoice = Invoice.objects.create(transaction=transaction, customer_code=customer_code, customer=customer)
            invoice_item = Invoice_Item.objects.create(invoice=invoice, price=price, quantity=quantity)

            return HttpResponseRedirect('/product/invoice_list/')
    else:
        form = Product_Sales_Form()

    context = {
        'form': form,
        'products':products,
    }

    return render(request, 'product/add_invoice_item.html', context)

def edit_product(request):
    # if this is a POST request we need to process the form data
      #兩種get取值方法都可以
    pid  = request.GET.get('pid')
    recd = Product.objects.get(id=pid)    
    form = ProductForm(instance=recd)
    return render(request,
                  'product/edit_product.html',
                  {'pid':pid,
                   'form': form})


def delete_product(request):
    #兩種get取值方法都可以
    pid = request.GET.get('pid')
    #myid = request.GET['myid']
     
    recd = Product.objects.get(id=pid)
    category_slug = recd.product_category.slug

    recd.delete()
    
    return HttpResponseRedirect('/product/'+category_slug)

def save_edit_product(request):
   pid  = request.POST['pid']
   products = Product.objects.get(id=pid)
   form = ProductForm(request.POST,  request.FILES, instance=products)
    
   if request.method=='POST':
       if form.is_valid():
            form.save()
            products = Product.objects.get(id=pid)
            #menu_item_category_id = recd.menu_category_id
            #category_recd=menu_category.objects.get(id=menu_item_category_id)
             
            # redirect to the detail page of the `Band` we just updated
            return HttpResponseRedirect('/product/product_list/')
       
       else:
            items='error'
            return render(request, 'show_test.html') 
   else:
           return HttpResponseRedirect('/product/product_list/')
   
def product_detail(request):
   
    pid = request.GET.get('pid')
    #myid = request.GET['myid']
     
    product = Product.objects.get(id=pid)
    
    return render(request, 'product/product-details.html', {
                                                    'product': product ,
                                                     })

def invoice_list(request):
    invoice_list = Invoice.objects.all()
    product      = Product.objects.all()
    paginator = Paginator(invoice_list, 6)  # 6 rows per page
    page = request.GET.get('page')
    invoices = paginator.get_page(page)
    total_records = paginator.count

    searchform_params = {
        'model': Invoice,
        'fields': ['transaction', 'customer', 'total', 'date_created', 'invoice_item__product__name','invoice_item__stock__quantity'],
        'label_suffixes': {
            'transaction': '交易編號',
            'customer': '客戶',
            'total': '總價',
            'date_created': '發票日期 ',
            'invoice_item__product__name': '商品名稱',
            'invoice_item__stock__quantity': '庫存數量',
        }
    }

    if request.method == 'POST':
        searchform = SearchForm(
            data=request.POST,
            **searchform_params
        )

        if searchform.is_valid():
            invoice_list = searchform.search()
            paginator = Paginator(invoice_list, 6)
            invoices = paginator.get_page(1)  # start at page 1 when initiating new search
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
        'invoices': invoices,
        'searchform': searchform,
        'total_records':total_records,
    }

    return render(request, 'product/invoice_list.html',context)
# First searchform is defined inside the POST block with data=request.POST.
# Second searchform is defined inside the same POST block after the search has been done with initial_data=request.GET.
# Third searchform is defined outside of the POST block with initial_data=request.GET.
# Each searchform definition is used for a different purpose:

# The first searchform is used to process the POST data and validate it.
# The second searchform is used to generate a new search form with the original search query data.
# The third searchform is used to generate the initial search form with the initial GET data.

def product_list(request):
    product_list = Product.objects.all()
    paginator = Paginator(product_list, 6)  # 6 rows per page
    page = request.GET.get('page')
    products = paginator.get_page(page)
    total_records = paginator.count

    

    searchform_params = {
        'model': Product,
        'fields': ['code', 'name', 'description', 'status','date_created','product_category'],
        'label_suffixes': {
            'code': '編號',
            'name': '名稱',
            'description': '產品說明',
            'status': '狀態',
            'date_created': '輸入日期 ',
            'product_category':'類別'
        }
        ,'category_fields': ['product_category'],  # 傳遞相應的類別欄位
    }

    if request.method == 'POST':
        searchform = SearchForm(
            data=request.POST,
            **searchform_params
        )

        if searchform.is_valid():
            product_list = searchform.search()
            paginator = Paginator(product_list, 6)
            products = paginator.get_page(1)  # start at page 1 when initiating new search
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
        'products': products,
        'searchform': searchform,
        'total_records':total_records,
    }


    return render(request, 'product/product_list.html', context)

def stock_list(request):
    product_list = Product.objects.all()
    paginator = Paginator(product_list, 6)  # 6 rows per page
    page = request.GET.get('page')
    products = paginator.get_page(page)
    total_records = paginator.count

    

    searchform_params = {
        'model': Product,
        'fields': ['code', 'name', 'description', 'status','date_created'],
        'label_suffixes': {
            'code': '編號',
            'name': '名稱',
            'description': '產品說明',
            'status': '狀態',
            'date_created': '輸入日期 ',
        }
    }

    if request.method == 'POST':
        searchform = SearchForm(
            data=request.POST,
            **searchform_params
        )

        if searchform.is_valid():
            product_list = searchform.search()
            paginator = Paginator(product_list, 6)
            products = paginator.get_page(1)  # start at page 1 when initiating new search
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
        'products': products,
        'searchform': searchform,
        'total_records':total_records,
    }


    return render(request, 'product/product_list.html', context)

def product_category_list(request):

    product_category_list = Product_category.objects.all()
    paginator = Paginator(product_category_list, 6)  # 6 rows per page
    page = request.GET.get('page')
    product_categorys = paginator.get_page(page)
    total_records = paginator.count


    searchform_params = {
        'model': Product_category,
        'fields': [ 'name','description'],
        'label_suffixes': {
            'name': '類別',
            'description': '說明',
        }
    }

    if request.method == 'POST':
        searchform = SearchForm(
            data=request.POST,
            **searchform_params
        )

        if searchform.is_valid():
            product_category_list = searchform.search()
            paginator = Paginator(product_category_list, 6)
            product_categorys = paginator.get_page(1)  # start at page 1 when initiating new search
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
        'product_categorys': product_categorys,
        'searchform': searchform,
        'total_records':total_records,
    }

    return render(request, 'product/product_category_list.html',context)






