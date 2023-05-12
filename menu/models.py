from django.urls import reverse
from django.db import models
from django.db.models import Count
import os

class Menu_category(models.Model):
    name = models.CharField(max_length=200,
                            db_index=True)
    slug = models.SlugField(max_length=200,
                            db_index=True,
                            unique=True)
                            

    class Meta:
        ordering = ('id',)
        verbose_name = 'menucategory'
        verbose_name_plural = 'menucategories'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('menu:menu_list_by_category',
                       args=[self.slug])

    def menu_items_count(self):
        return self.menu_item.annotate(count=Count('menu_category')).count()

def menu_item_image_upload_path(instance, filename):
    """
    Returns the upload path for the image field of a Menu_item instance.
    The image is uploaded to a folder named after the Menu_category's slug.
    """
    return os.path.join('menu_items', instance.menu_category.slug, filename)

class Menu_item(models.Model):
    # Fields
    menu_category       = models.ForeignKey(Menu_category,on_delete=models.CASCADE,                                 
                                 related_name='menu_item')
    menu_title          = models.CharField(max_length=20,null=False)
    menu_description    = models.TextField(blank=False)
    price               = models.DecimalField(max_digits=10, decimal_places=0)
    menu_created_user   = models.CharField(max_length=50,null=False)
    image               = models.ImageField(upload_to=menu_item_image_upload_path)
    menu_created        = models.DateTimeField(auto_now=True)
    menu_likes          = models.IntegerField(default=0)
    menu_hates          = models.IntegerField(default=0)
   
    

    class Meta:
        ordering = ('-id',)

    def slug(self):
        return self.menu_category.slug   
    
    def likes(self):  # 案讚+1
      self.menu_likes += 1
      self.save(update_fields=['menu_likes'])

    def hates(self):
      self.menu_hates += 1
      self.save(update_fields=['menu_hates'])
       
     
    def __str__(self):
      return self.menu_title

    def menu_comments_count(self):
        return self.menu_comments.annotate(count=Count('menu_item')).count()
    
class Comment_item(models.Model): 
    menu_item = models.ForeignKey(Menu_item, on_delete=models.CASCADE,
                                   related_name='menu_comments', null=True)
    bid          = models.IntegerField(null=False)
    name         = models.CharField(max_length=50,null=False)
    email        = models.TextField(blank=False)
    comment      = models.TextField(blank=False)
    website      = models.CharField(max_length=50,null=False)
    comment_created = models.DateTimeField(auto_now=True)
    

    class Meta:
        ordering = ('-id',)
    
    def __str__(self):
        return self.name

    