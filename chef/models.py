from django.db import models
from django.urls import reverse
import os
# Create your models here.


def chef_image_upload_path(instance,filename):
    """
    Returns the upload path for the image field of a Chef instance.

    """
    return os.path.join('chef', filename)

class Chef(models.Model):
    chef_name = models.CharField(max_length=100)
    chef_title = models.CharField(max_length=100)
    chef_img = models.ImageField(upload_to=chef_image_upload_path, null=True, blank=True)
    chef_profile = models.TextField()

    class Meta:
      ordering = ('id',)

    def __str__(self):
      return self.chef_name