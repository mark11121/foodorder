# Generated by Django 4.1.7 on 2023-06-05 06:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0014_customer_password"),
    ]

    operations = [
        migrations.AlterField(
            model_name="customer",
            name="email",
            field=models.EmailField(max_length=100, unique=True),
        ),
    ]
