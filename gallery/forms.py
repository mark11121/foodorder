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




   