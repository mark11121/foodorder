from django.dispatch import receiver
from django.urls import reverse
from django.db import models
from django.db.models import Count
import os
from django.db.models import Sum
from django.utils import timezone

 
# Create your models here.

class Product_category(models.Model):
    name = models.CharField(max_length=250)
    slug = models.SlugField(max_length=200,
                            db_index=True,
                            unique=True)
    description = models.TextField()
    status = models.CharField(max_length=2, choices=(('1','Active'),('2','Inactive')), default=1)
    date_created = models.DateTimeField(auto_now=True)
    date_updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('id',)
        verbose_name = 'productcategory'
        verbose_name_plural = 'productcategories'

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('product:product_list_by_category', args=[self.slug])

    def product_items_count(self):
        return self.product_item.annotate(count=Count('product_category')).count()
         

def product_image_upload_path(instance, filename):
    """
    Returns the upload path for the image field of a product_item instance.
    The image is uploaded to a folder named after the product_category's slug.
    """
    return os.path.join('product', instance.product_category.slug, filename)

class Product(models.Model):
    product_category = models.ForeignKey(Product_category, on_delete=models.CASCADE, related_name='product_item', default=1)
    code=models.CharField(max_length=100,null=False,default='')
    name=models.CharField(max_length=250,null=False,default='')
    description = models.TextField()
    price = models.FloatField(default=0)
    image = models.ImageField(upload_to=product_image_upload_path)
    user_created=models.CharField(max_length=100,blank=True, null=True)
    status = models.CharField(max_length=2, choices=(('1','Active'),('2','Inactive')), default=1)
    date_created = models.DateTimeField(auto_now=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.code + ' - ' + self.name

    def count_inventory(self):
        stocks = Stock.objects.filter(product = self)
        stockIn = 0
        stockOut = 0
        for stock in stocks:
            if stock.type == '1':
                stockIn = int(stockIn) + int(stock.quantity)
            else:
                stockOut = int(stockOut) + int(stock.quantity)
        available  = stockIn - stockOut
        return available
    
class Stock(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.FloatField(default=0)
    type = models.CharField(max_length=2,choices=(('1','Stock-in'),('2','Stock-Out')), default = 1)
    date_created = models.DateTimeField(auto_now=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product.code + ' - ' + self.product.name



class Invoice(models.Model):
    transaction = models.CharField(max_length = 250)
    customer_code = models.CharField(max_length = 20)
    customer = models.CharField(max_length = 250)
    total = models.FloatField(default= 0)
    date_created = models.DateTimeField(default=timezone.now)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.transaction

    def item_count(self):
        return Invoice_Item.objects.filter(invoice = self).aggregate(Sum('quantity'))['quantity__sum']

class Invoice_Item(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE,default=1)
    name    = models.CharField(max_length=250,null=False,default='') 
    stock   = models.ForeignKey(Stock, on_delete=models.CASCADE, blank= True, null= True)
    price   = models.FloatField(default=0)
    quantity = models.FloatField(default=0)

    def __str__(self):
        return self.invoice.transaction


@receiver(models.signals.post_save, sender=Invoice_Item)
def stock_update(sender, instance, **kwargs):
    stock = Stock(product = instance.product, quantity = instance.quantity, type = 2)
    stock.save()
    # stockID = Stock.objects.last().id
    Invoice_Item.objects.filter(id= instance.id).update(stock=stock)

@receiver(models.signals.post_delete, sender=Invoice_Item)
def delete_stock(sender, instance, **kwargs):
    try:
        stock = Stock.objects.get(id=instance.stock.id).delete()
    except:
        return instance.stock.id



    
    