# Generated by Django 4.1.7 on 2023-04-21 00:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment_item',
            name='blog_item',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='blog_item', to='blog.blog_item'),
        ),
    ]
