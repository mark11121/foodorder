from datetime import timezone
from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import pre_save

# Create your models here.
class Profile(models.Model):
   user = models.OneToOneField(User, on_delete=models.CASCADE)
   cellphone = models.CharField(max_length=50)
   birthdate = models.DateField(verbose_name="出生日期")
   address   = models.CharField(max_length=100)


from django.db import models
from django.contrib.auth.models import User

class Customer(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('credit_card', 'Credit Card'),
        ('paypal', 'PayPal'),
        ('check', 'Check'),
        ('bank_transfer', 'Bank Transfer'),
    ]
    customer_code = models.CharField(max_length=20, unique=True, editable=False)
    first_name = models.CharField(max_length=100, default='')
    last_name = models.CharField(max_length=100, default='')
    gender = models.CharField(max_length=10, choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')],default='')

    cellphone = models.CharField(max_length=50)
    birthdate = models.DateField(verbose_name="出生日期")
    address = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    company = models.CharField(max_length=100, blank=True)
    job_title = models.CharField(max_length=100 ,blank=True)
    notes = models.TextField(blank=True)

    # Billing information
    payment_method = models.CharField(max_length=50, choices=PAYMENT_METHOD_CHOICES)
    use_billing_address = models.BooleanField(default=False)
    billing_address = models.CharField(max_length=100, blank=True)
    card_number = models.CharField(max_length=16, blank=True)
    card_expiration_date = models.CharField(max_length=7, blank=True)
    card_cvv = models.CharField(max_length=4, blank=True)

    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        if self.use_billing_address:
            self.billing_address = self.address
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.customer_code} {self.first_name} {self.last_name}"

@receiver(pre_save, sender=Customer)
def customer_pre_save(sender, instance, *args, **kwargs):
    if not instance.customer_code:
        today = timezone.now().strftime('%Y%m%d')
        last_customer = sender.objects.filter(customer_code__startswith=today).order_by('-customer_code').first()
        if last_customer:
            last_code = int(last_customer.customer_code.split('-')[1])
            new_code = f"{today}-{str(last_code+1).zfill(6)}"
        else:
            new_code = f"{today}-000001"
        instance.customer_code = new_code        