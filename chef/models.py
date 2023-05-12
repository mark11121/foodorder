from django.db import models
from django.urls import reverse
# Create your models here.

class Chef(models.Model):
    chef_name = models.CharField(max_length=100)
    chef_title = models.CharField(max_length=100)
    chef_img = models.ImageField(upload_to='')
    chef_profile = models.TextField()

    class Meta:
      ordering = ('id',)

    def __str__(self):
      return self.chef_name