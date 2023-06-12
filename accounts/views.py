from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from accounts.forms import *
from django.contrib.auth.models import User
from accounts.models import Profile,Customer
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.core.paginator import Paginator
from django.db.models import Q
import os
from chef import form
from main.form import SearchForm
from django.contrib.auth.views import LoginView


def signup_new_view(request):
    if request.method == 'POST':
        uform  = NewUSerForm(request.POST)
        pform  = ProfileForm(request.POST)
        searchform = Search_User_Form(request.POST)
        if uform.is_valid() and pform.is_valid():

            user  = uform.save()
            pform = pform.save(commit=False)
            pform.user = user
            pform.save()
            users = User.objects.all()
            return render(request, 'accounts/user_list.html', {'users': users,'searchform':searchform})        
    else:
        uform = NewUSerForm(request.POST)
        pform = ProfileForm(request.POST)

    return render(request, 'accounts/signup_new.html', { 'uform': uform,'pform': pform  })
    


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if 'next' in request.POST:
                return redirect(request.POST.get('next'))
            return redirect('/')
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', { 'form': form })

def logout_view(request):
    
    logout(request)
    
    return redirect('/')


def make_superuser(request, user_id):
    user = User.objects.get(id=user_id)
    user.is_superuser = True
    user.save()
    return redirect('/accounts/user_list/') # redirect to user list page after setting the user to superuser

def del_superuser(request, user_id):
    user = User.objects.get(id=user_id)
    user.is_superuser = False
    user.save()
    return redirect('/accounts/user_list/') # redirect to user list page after setting the user to superuser

def edit_profile(request, user_id):
    profile = get_object_or_404(Profile, id=user_id)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('accounts/user_list/')
    else:
        form = ProfileForm(instance=profile)

    context = {'form': form, 'pid': user_id}
    return render(request, 'accounts/edit_profile.html', context)

def save_edit_profile(request):
   pid  = request.POST['pid']
   recd = Profile.objects.get(id=pid)
   form = ProfileForm(request.POST,  request.FILES, instance=recd)
   
   if request.method=='POST':
       if form.is_valid():
            form.save()
            # redirect to the detail page of the `Band` we just updated
            return HttpResponseRedirect('/accounts/user_list/')
       else:
            items='error'
            return render(request, 'show_test.html', locals()) 
   else:
        return HttpResponseRedirect('/')   
          
   return render(request, 'accounts/edit_profile.html', context)

def add_profile(request, user_id):
    
    if request.method == 'POST':
        form = add_ProfileForm(request.POST, request.FILES)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user_id = user_id
            profile.save()
            return HttpResponseRedirect('/accounts/user_list/')
    else:
        form = ProfileForm()

    context = {'form': form, 'user_id': user_id}

    return render(request, 'accounts/add_profile.html', context)

def del_profile(request, user_id):
    
    try:
        user = User.objects.get(id=user_id)
        profile = Profile.objects.get(user=user)
        profile.delete()
        return HttpResponseRedirect('/accounts/user_list/')
    except User.DoesNotExist:
        return HttpResponse("User does not exist")
    except Profile.DoesNotExist:
        return HttpResponse("Profile does not exist")
    

def del_user(request, user_id):
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return HttpResponse("User does not exist")
    
    try:
        profile = Profile.objects.get(user=user)
    except Profile.DoesNotExist:
        pass
    else:
        profile.delete()

    user.delete()

    return HttpResponseRedirect('/accounts/user_list/')
        
#驗證是否登入(員工或客戶)
def customer_or_user_login_required(view_func):
    def wrapper(request, *args, **kwargs):
        customer_id = request.session.get('customer_id')
        user_id = request.session.get('user_id')
        
        if customer_id or user_id:
            # Customer或User其中一种已登录
            return view_func(request, *args, **kwargs)
        elif request.user.is_authenticated:
            # 使用django内建的User进行验证
            return view_func(request, *args, **kwargs)
        else:
            # 未登录，重定向到登录页面或其他处理方式
            return redirect('/accounts/cust_login/')  # 根据您的URL设置进行重定向

    return wrapper

#驗證是否登入(客戶)
def customer_login_required(view_func):
    def wrapper(request, *args, **kwargs):
        customer_id = request.session.get('customer_id')
        if customer_id:
            # Customer已登录
            return view_func(request, *args, **kwargs)
        else:
            # 未登录，重定向到登录页面或其他处理方式
            return redirect('/accounts/cust_login/')  # 根据您的URL设置进行重定向

    return wrapper



def cust_login(request):
    customer_id = request.session.get('customer_id')

    if customer_id:
        # 用户已登录，重定向到首页
        return redirect('/')  # 替换为您实际定义的首页URL名称

    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        
        # 檢查用戶名和密碼是否匹配
        try:
            customer = Customer.objects.get(email=email, password=password)
        except Customer.DoesNotExist:
            customer = None
        
        if customer:
            # 登录成功，执行相应的操作，例如设置用户登录状态
            request.session['customer_id'] = customer.id
            request.session['last_name'] = customer.last_name  # 将姓氏存储在session中
            
            # 重定向到登录成功后的页面
            return redirect('/')
        else:
            # 登录失败，显示错误消息
            error_message = 'Invalid email or password.'
            return render(request, 'accounts/cust_login.html', {'error_message': error_message})
    else:
        customer_id = request.session.get('customer_id')
        context = {}
        
        if customer_id:
            # 用户已登录
            context['is_logged_in'] = True
        else:
            # 用户未登录
            context['is_logged_in'] = False
        
        return render(request, 'accounts/cust_login.html', context)
    

def cust_logout(request):
    del request.session['customer_id']
    # 执行其他登出操作
    
    # 重定向到登出成功后的页面
    return redirect('/accounts/cust_login/')


def create_customer(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            customer = form.save(commit=False)
            # generate and set the customer code
            today = timezone.datetime.today().strftime('%Y%m%d')
            last_customer = Customer.objects.filter(customer_code__startswith=today).order_by('-customer_code').first()
            if last_customer:
                last_code = int(last_customer.customer_code.split('-')[1])
                new_code = f"{today}-{str(last_code+1).zfill(6)}"
            else:
                new_code = f"{today}-000001"
            customer.customer_code = new_code
            # save the customer
            customer.save()
            customers = Customer.objects.all()
            return redirect('/accounts/customer_list/')
    else:
        form = CustomerForm()

    return render(request, 'accounts/create_customer.html', {'form': form})


def edit_customer(request, pid):
    customer = Customer.objects.get(id=pid)

    if request.method == 'POST':
        if len(request.FILES) !=0:
            if customer.customer_img and len(customer.customer_img) > 0:
                os.remove(customer.customer_img.path)
            customer.customer_img = request.FILES['customer_img']

        # Check if delete_image checkbox is selected
        if 'delete_image' in request.POST:
            if len(customer.customer_img) > 0:
                os.remove(customer.customer_img.path)
            customer.customer_img = None

        customer.customer_code  = request.POST.get('customer_code')
        customer.first_name     = request.POST.get('first_name')
        customer.last_name      = request.POST.get('last_name')
        customer.gender         = request.POST.get('gender')
        customer.cellphone      = request.POST.get('cellphone')
        customer.birthdate      = request.POST.get('birthdate')
        customer.address        = request.POST.get('address')
        customer.email          = request.POST.get('email')
        customer.company        = request.POST.get('company')
        customer.job_title      = request.POST.get('job_title')
        customer.notes          = request.POST.get('notes')
        customer.save()
        return HttpResponseRedirect('/accounts/customer_list/')

    context = {'customer':customer}
    return render(request,'accounts/edit_customer.html',context)



def customer_detail(request, pk):
    customer = Customer.objects.get(pk=pk)
    return render(request, 'accounts/customer_detail.html', {'customer': customer})    
    

def delete_customer(request):
    #兩種get取值方法都可以
    pid = request.GET.get('pid')
    #myid = request.GET['myid']
     
    res = Customer.objects.get(id=pid)
#    if res.customer_img and len(res.customer_img)>= 0:
#       os.remove(res.customer_img.path)
    res.delete()
    
    return HttpResponseRedirect('/accounts/customer_list/')



# First searchform is defined inside the POST block with data=request.POST.
# Second searchform is defined inside the same POST block after the search has been done with initial_data=request.GET.
# Third searchform is defined outside of the POST block with initial_data=request.GET.
# Each searchform definition is used for a different purpose:

# The first searchform is used to process the POST data and validate it.
# The second searchform is used to generate a new search form with the original search query data.
# The third searchform is used to generate the initial search form with the initial GET data.

def user_list(request):
    user_list = User.objects.all()
    paginator = Paginator(user_list, 6)  # 6 rows per page
    page = request.GET.get('page')
    users = paginator.get_page(page)
    total_records = paginator.count

    searchform_params = {
        'model': User,
        'fields': ['username', 'first_name', 'last_name'],
        'label_suffixes': {
            'username': '用戶名稱',
            'first_name': '名字',
            'last_name': '姓',
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

            user_list = User.objects.filter(**search_params)
            paginator = Paginator(user_list, 6)
            users = paginator.get_page(1)  # start at page 1 when initiating new search
            total_records = paginator.count

    else:
        searchform = SearchForm(
            initial_data=request.GET,
            **searchform_params
        )

    context = {
        'users': users,
        'searchform': searchform,
        'total_records':total_records,
        'searchform_params': searchform_params,  # 添加 searchform_params 到上下文
    }

    return render(request, 'accounts/user_list.html', context)


def customer_list(request):
    customer_list = Customer.objects.all()
    paginator = Paginator(customer_list, 6)  # 6 rows per page
    page = request.GET.get('page')
    customers = paginator.get_page(page)
    total_records = paginator.count

    searchform_params = {
        'model': Customer,
        'fields': ['customer_code','first_name', 'last_name','cellphone'],
        'label_suffixes': {
            'customer_code': '用戶編號',
            'last_name': '姓',
            'first_name': '名字',
            'cellphone': '手機',
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

            customer_list = Customer.objects.filter(**search_params)
            paginator = Paginator(customer_list, 6)
            customers = paginator.get_page(1)  # start at page 1 when initiating new search
            total_records = paginator.count

    else:
        searchform = SearchForm(
            initial_data=request.GET,
            **searchform_params
        )

    context = {
        'customers': customers,
        'searchform': searchform,
        'total_records':total_records,
        'searchform_params': searchform_params,  # 添加 searchform_params 到上下文
    }    

    return render(request, 'accounts/customer_list.html', context)