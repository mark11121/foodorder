from django import forms
from chef.models import *

class ChefForm(forms.ModelForm):

    chef_img = forms.ImageField(required=False) 
    
    class Meta:
        model =  Chef
        fields = ['chef_name','chef_title','chef_img','chef_profile']

        labels = {
            'chef_name': '廚師名稱',
            'chef_title': '廚師頭銜',
            'chef_img': '廚師照片',
            'chef_profile':'廚師介紹',
        }
