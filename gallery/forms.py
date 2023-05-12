from django import forms
from django.contrib.auth.forms import UserCreationForm,PasswordChangeForm, UserChangeForm

from django import forms
from gallery.models import *


class PhotoCategoryForm(forms.ModelForm):
     
    class Meta:
        model =  Photo_category
        fields = '__all__'

        labels = {
            'name': '類別',
        }        

class PhotoForm(forms.ModelForm):

    image = forms.ImageField(required=False) 
    
    class Meta:
        model =  Photo
        fields = ['photo_category','title','description','image']

        labels = {
            'photo_category': '類別',
            'title': '標題',
            'description': '說明',
            'image':'上傳圖檔',

        }        


        
class Search_Photo_Category_Form(forms.ModelForm):
    name = forms.CharField(required=False, label='類別')

    class Meta:
        model = Photo
        fields = ['name']
        widgets = {
            'name': forms.TextInput(),

        }

    

class Search_Photo_Form(forms.ModelForm):
    photo_category = forms.CharField(required=False, label='類別')
    title          = forms.CharField(required=False, label='標題')
    description    = forms.CharField(required=False, label='說明')


    class Meta:
        model = Photo
        fields = ['photo_category', 'title', 'description']
        widgets = {
            'photo_category': forms.TextInput(),
            'title': forms.TextInput(),
            'description': forms.Textarea(),
        }



   