from django.dispatch import receiver
from django.urls import reverse
from django.db import models
from django.db.models import Count
import os
from django.db.models import Sum
from django.utils import timezone
from django.db.models.signals import pre_save

 
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
    
    def get_absolute_url_2(self):
        return reverse('product:product_list_by_category_2', args=[self.slug])

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


@receiver(pre_save, sender=Product)
def product_pre_save(sender, instance, *args, **kwargs):
    if not instance.code:
        
        last_product = sender.objects.order_by('-code').first()
        if last_product:
            last_code = int(last_product.code)
            new_code = f"{str(last_code+1).zfill(6)}"
        else:
            new_code = '000001'
        instance.code = new_code 



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



    
class Product_sales(models.Model):
    customer_code = models.CharField(max_length=20)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    cellphone = models.CharField(max_length=20)
    email = models.EmailField()
    address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return self.customer_code

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())
    

class OrderItem(models.Model):
    order = models.ForeignKey(Product_sales,on_delete=models.CASCADE,related_name='items')
    product = models.ForeignKey(Product,on_delete=models.CASCADE,related_name='order_items')
    # 台灣價錢都是整數，所以可以設定 decimal_places=0
    price = models.DecimalField(max_digits=10, decimal_places=0)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return '{}'.format(self.id)

    def get_cost(self):
        return self.price * self.quantity