from django import forms
from django_select2.forms import ModelSelect2Widget
from django_select2.forms import Select2Widget
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm, UserChangeForm
from product.models import Product_category, Product, Invoice
from accounts.models import Customer


class ProductCategoryForm(forms.ModelForm):

    class Meta:
        model = Product_category
        fields = '__all__'

        labels = {
            'name': '類別',
        }        

class ProductForm(forms.ModelForm):

    image = forms.ImageField(required=False) 
    
    class Meta:
        model = Product
        fields = ['product_category', 'code', 'name', 'description', 'user_created', 'price', 'status', 'image']

        labels = {
            'product_category': '產品類別',
            'code': '產品編號',
            'name': '產品名稱',
            'description': '產品說明',
            'user_created':'建單人',
            'image':'上傳圖檔',
            'price':'售價',
        }        


class InvoiceForm(forms.ModelForm):
 
    class Meta:
        model = Invoice
        fields = ['transaction', 'customer', 'date_created']
        labels = {
            'transaction': '交易編號',
            'customer': '客戶',
            'date_created': '交易日期',
        }  


class Product_Sales_Form(forms.ModelForm):

    customer_code = forms.CharField(required=False, label='客戶編號', widget=forms.TextInput(attrs={'id': 'customer_code'}))
    customer = forms.CharField(required=False, label='客戶名字', widget=forms.TextInput(attrs={'id': 'customer'}))
    transaction = forms.CharField(required=False, label='交易編號')
    #product = forms.ModelChoiceField(queryset=Product.objects.all(), label='產品')
    code     = forms.CharField(required=False, label='產品編號', widget=forms.TextInput(attrs={'id': 'product_code'}))
    name     = forms.CharField(required=False, label='產品名稱', widget=forms.TextInput(attrs={'id': 'product_name'}))

    quantity = forms.FloatField(label='數量')
    price    = forms.FloatField(required=False, label='產品價錢', widget=forms.TextInput(attrs={'id': 'product_price'}))
    
    
    class Meta:
        model = Invoice
        fields = ['customer_code', 'customer', 'transaction','code','name','price','quantity']
        widgets = {
            'transaction': forms.TextInput(),
        }
        
class Search_Product_Category_Form(forms.ModelForm):
    name = forms.CharField(required=False, label='類別')

    class Meta:
        model = Product_category
        fields = ['name']
        widgets = {
            'name': forms.TextInput(),

        }