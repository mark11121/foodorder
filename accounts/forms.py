from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile
from accounts.models import Customer

class NewUSerForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone_number = forms.CharField(required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    
    class Meta:
        model = User
        fields = ("username", "email", "phone_number", "first_name","last_name", "password1", "password2")

    def save(self,commit=True):
        user = super(NewUSerForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        user.phone_number = self.cleaned_data["phone_number"]
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        
        if commit:
            user.save()
        return user
    
class ProfileForm(forms.ModelForm):

      class Meta:
            model = Profile
            fields = ['birthdate', 'cellphone','address']
            widgets = {
            'birthdate': forms.DateInput(attrs={'placeholder': 'YYYY-MM-DD'}),
            }
      
      def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['address'].required = False
        self.fields['cellphone'].required = False
        self.fields['birthdate'].required = False       

class add_ProfileForm(forms.ModelForm):

      class Meta:
            model = Profile
            fields = ['birthdate', 'cellphone','address']
            widgets = {
            'birthdate': forms.DateInput(attrs={'placeholder': 'YYYY-MM-DD'}),
            }
      
      def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['address'].required = False
        self.fields['cellphone'].required = False
        self.fields['birthdate'].required = False               



class CustomerForm(forms.ModelForm):
    PAYMENT_METHOD_CHOICES = [
        ('credit_card', 'Credit Card'),
        ('paypal', 'PayPal'),
        ('check', 'Check'),
        ('bank_transfer', 'Bank Transfer'),
    ]
    
    gender_choices = [('M', 'Male'), ('F', 'Female'), ('O', 'Other')]
    first_name = forms.CharField(max_length=100, label='名字', required=True)
    last_name = forms.CharField(max_length=100, label='姓氏', required=True)
    email = forms.EmailField(label='Email', required=False)
    gender = forms.ChoiceField(choices=gender_choices, widget=forms.Select, label='性别', required=False)
    
    cellphone = forms.CharField(max_length=50, label='手機', required=False)
    birthdate = forms.DateField(label='出生日期', required=False, widget=forms.SelectDateWidget(years=range(1900, 2023)))
    address = forms.CharField(max_length=100, label='地址', required=False)
    company = forms.CharField(max_length=100, label='公司', required=False)
    job_title = forms.CharField(max_length=100, label='職稱', required=False)
    notes = forms.CharField(widget=forms.Textarea, required=False, label='備註')
    

    # Billing information
    payment_method = forms.ChoiceField(choices=PAYMENT_METHOD_CHOICES, widget=forms.Select, label='付款方式', required=False)
    use_billing_address = forms.BooleanField(required=False, widget=forms.CheckboxInput, label='使用帳單地址')
    billing_address = forms.CharField(max_length=100, required=False, label='帳單地址')
    card_number = forms.CharField(max_length=16, required=False, label='信用卡號')
    card_expiration_date = forms.CharField(max_length=7, required=False, label='有效期')
    card_cvv = forms.CharField(max_length=4, required=False, label='CVV碼')

    class Meta:
        model = Customer
        fields = ['customer_code','first_name', 'last_name', 'email', 'gender',
                  'cellphone', 'birthdate', 'address', 'company',
                  'job_title','notes','payment_method', 'use_billing_address',
                  'billing_address', 'card_number', 'card_expiration_date', 'card_cvv']
        exclude = ['customer_code'] # exclude the non-editable field

class Search_Customer_Form(forms.ModelForm):
    
    first_name = forms.CharField(required=False, label='名字')
    last_name = forms.FloatField(required=False, label='姓')
    email = forms.EmailField(required=False, label='Email')
    company = forms.CharField(required=False, label='任職公司')

    class Meta:
        model = Customer
        fields = ['first_name', 'last_name', 'email','company']
        widgets = {
           
            'first_name': forms.TextInput(),
            'last_name': forms.NumberInput(),
            'email': forms.EmailInput(),
            'company':forms.TextInput(),
        }

class Search_User_Form(forms.ModelForm):
    
    first_name = forms.CharField(required=False, label='名字')
    last_name = forms.CharField(required=False, label='姓')
    username = forms.CharField(required=False, label='用戶名稱')
    

    class Meta:
        model = Customer
        fields = ['first_name', 'last_name', 'username']
        widgets = {
           
            'first_name': forms.TextInput(),
            'last_name': forms.TextInput(),
            'username': forms.TextInput(),
            
        }

        