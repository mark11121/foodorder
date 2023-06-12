from django.db.models import Count
from django.urls import reverse
from django.db import models
import os

class Blog_category(models.Model):
    name = models.CharField(max_length=200,
                            db_index=True)
    slug = models.SlugField(max_length=200,
                            db_index=True,
                            unique=True)
                            

    class Meta:
        ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('blog:blog_list_by_category',
                       args=[self.slug])

    def blog_items_count(self):
        return self.blog_item.annotate(count=Count('blog_category')).count()


def blog_image_upload_path(instance, filename):
    """
    Returns the upload path for the image field of a blog_item instance.
    The image is uploaded to a folder named after the blog_category's slug.
    """
    return os.path.join('blog', instance.blog_category.slug, filename)

class Blog_item(models.Model):
    blog_category = models.ForeignKey(Blog_category,on_delete=models.CASCADE,                                 
                                 related_name='blog_item')
    blog_title          = models.CharField(max_length=50,null=False)
    blog_content        = models.TextField(blank=False)
    blog_user           = models.CharField(max_length=50,null=False)
    image               = models.ImageField(upload_to=blog_image_upload_path, null=True, blank=True)
    blog_created        = models.DateTimeField(auto_now=True)
    blog_likes          = models.IntegerField(default=0)
    blog_hates          = models.IntegerField(default=0)
   
    

    class Meta:
        ordering = ('-id',)

    def slug(self):
        return self.blog_category.slug   
    
    def likes(self):  # 案讚+1
      self.blog_likes += 1
      self.save(update_fields=['blog_likes'])

    def hates(self):
      self.blog_hates += 1
      self.save(update_fields=['blog_hates'])
       
     
    def __str__(self):
      return self.blog_title

    def blog_comments_count(self):
        return self.blog_comments.annotate(count=Count('blog_item')).count()
    
class Comment_item(models.Model): 
    blog_item = models.ForeignKey(Blog_item, on_delete=models.CASCADE,
                                   related_name='blog_comments', null=True)
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

    