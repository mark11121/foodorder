# Generated by Django 4.1.7 on 2023-05-01 06:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("chef", "0002_chef_chef_title"),
    ]

    operations = [
        migrations.AlterField(
            model_name="chef",
            name="chef_title",
            field=models.CharField(max_length=100),
        ),
    ]
