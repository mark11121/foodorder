from django.db import models
import os
# Create your models here.

class Photo_category(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True, unique=True)
                            
    class Meta:
        ordering = ('id',)
        verbose_name = 'photocategory'
        verbose_name_plural = 'photocategories'

    def __str__(self):
        return self.name

def photo_image_upload_path(instance, filename):
    """
    Returns the upload path for the image field of a Photo instance.
    The image is uploaded to a folder named after the Photo_category's slug.
    """
    return os.path.join('photo_gallery', instance.photo_category.slug, filename)

class Photo(models.Model):
    photo_category = models.ForeignKey(Photo_category,on_delete=models.CASCADE, null=True, blank=True, related_name='photo')
    title          = models.CharField(max_length=200)
    description    = models.TextField(null=True, blank=True)
    image          = models.ImageField(upload_to=photo_image_upload_path)

    def __str__(self):
        return self.title
    
