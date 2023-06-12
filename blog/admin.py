from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Blog_item)
admin.site.register(Blog_category)
admin.site.register(Comment_item)