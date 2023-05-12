from braintree import Customer
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

from chef import form
from main.form import SearchForm

def signup_view(request):
    if request.method == 'POST':
        uform  = NewUSerForm(request.POST)
        pform = ProfileForm(request.POST)
        if uform.is_valid() and pform.is_valid():
            user  = uform.save()
            pform = pform.save(commit=False)
            pform.user = user
            pform.save()
            login(request, user)
            return redirect('/')
    else:
        uform = NewUSerForm(request.POST)
        pform = ProfileForm(request.POST)
    return render(request, 'accounts/signup.html', { 'uform': uform,'pform': pform  })

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
    }
    if request.method == 'POST':
        searchform = SearchForm(
            data=request.POST,
            **searchform_params
        )

        if searchform.is_valid():
            user_list = searchform.search()
            paginator = Paginator(user_list, 6)
            users = paginator.get_page(1)  # start at page 1 when initiating new search
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
        'users': users,
        'searchform': searchform,
        'total_records':total_records,
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
    }
    if request.method == 'POST':
        searchform = SearchForm(
            data=request.POST,
            **searchform_params
        )

        if searchform.is_valid():
            customer_list = searchform.search()
            paginator = Paginator(customer_list, 6)
            customers = paginator.get_page(1)  # start at page 1 when initiating new search
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
        'customers': customers,
        'searchform': searchform,
        'total_records':total_records,
    }    

    return render(request, 'accounts/customer_list.html', context)


    

def make_superuser(request, user_id):
    user = User.objects.get(id=user_id)
    user.is_superuser = True
    user.save()
    return redirect('/accounts/users/') # redirect to user list page after setting the user to superuser

def del_superuser(request, user_id):
    user = User.objects.get(id=user_id)
    user.is_superuser = False
    user.save()
    return redirect('/accounts/users/') # redirect to user list page after setting the user to superuser

def edit_profile(request, user_id):
    profile = get_object_or_404(Profile, id=user_id)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('user_list')
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
            return HttpResponseRedirect('/accounts/users/')
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
            return HttpResponseRedirect('/accounts/users/')
    else:
        form = ProfileForm()

    context = {'form': form, 'user_id': user_id}

    return render(request, 'accounts/add_profile.html', context)

def del_profile(request, user_id):
    
    try:
        user = User.objects.get(id=user_id)
        profile = Profile.objects.get(user=user)
        profile.delete()
        return HttpResponseRedirect('/accounts/users/')
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


def edit_customer(request, pk):
    customer = Customer.objects.get(pk=pk)
    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            customer = form.save(commit=False)
            customer.save()
            return redirect('/accounts/customer_detail/', pk=customer.pk)
    else:
        form = CustomerForm(instance=customer)

    return render(request, 'edit_customer.html', {'form': form, 'customer': customer})


def customer_detail(request, pk):
    customer = Customer.objects.get(pk=pk)
    return render(request, 'accounts/customer_detail.html', {'customer': customer})    
    