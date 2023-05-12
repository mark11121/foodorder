from django import forms
from blog.models import Blog_item,Blog_category,Comment_item

class BlogForm(forms.ModelForm):

    image = forms.ImageField(required=False) 
    
    class Meta:
        model =  Blog_item
        fields = ['blog_category','blog_title','blog_content','blog_user','image']

        labels = {
            'blog_category': '類別',
            'blog_title': '重點標題',
            'blog_content': '內容',
            'blog_user':'發表人',
            'image':'上傳圖檔',
        }

class BlogCategoryForm(forms.ModelForm):
     
    class Meta:
        model =  Blog_category
        fields = '__all__'

        labels = {
            'blog_category': '類別',
        }        

class CommentForm(forms.ModelForm):
     
    class Meta:
        model =  Comment_item
        fields = '__all__'
        labels = {
            'name': '姓名',
            'email': 'eMain',
            'website': '網址1',
            'comment':'回應內容',
        }        