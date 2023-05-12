from django import forms
from menu.models import Menu_item,Menu_category,Comment_item

class MenuForm(forms.ModelForm):

    image = forms.ImageField(required=False) 
    
    class Meta:
        model =  Menu_item
        fields = ['menu_category','menu_title','menu_description','menu_created_user','price','image']

        labels = {
            'menu_category': '菜單類別',
            'menu_title': '菜單標題',
            'menu_description': '菜單說明',
            'menu_created_user':'建單人',
            'image':'上傳圖檔',
            'price':'售價',
        }

class MenuCategoryForm(forms.ModelForm):
     
    class Meta:
        model =  Menu_category
        fields = '__all__'

        labels = {
            'menu_category': '類別',
        }        

class CommentForm(forms.ModelForm):
     
    class Meta:
        model =  Comment_item
        fields = '__all__'
        labels = {
            'name': '姓名',
            'email': 'eMain',
            'comment':'回應內容',
        }        