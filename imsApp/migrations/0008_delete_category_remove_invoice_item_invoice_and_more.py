# Generated by Django 4.2.1 on 2023-05-07 03:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('imsApp', '0007_invoice_date_created_invoice_date_updated'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Category',
        ),
        migrations.RemoveField(
            model_name='invoice_item',
            name='invoice',
        ),
        migrations.RemoveField(
            model_name='invoice_item',
            name='product',
        ),
        migrations.RemoveField(
            model_name='invoice_item',
            name='stock',
        ),
        migrations.RemoveField(
            model_name='stock',
            name='product',
        ),
        migrations.DeleteModel(
            name='Invoice',
        ),
        migrations.DeleteModel(
            name='Invoice_Item',
        ),
        migrations.DeleteModel(
            name='Product',
        ),
        migrations.DeleteModel(
            name='Stock',
        ),
    ]