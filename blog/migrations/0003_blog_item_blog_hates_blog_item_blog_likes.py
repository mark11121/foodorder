# Generated by Django 4.1.7 on 2023-04-21 01:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_alter_comment_item_blog_item'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog_item',
            name='blog_hates',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='blog_item',
            name='blog_likes',
            field=models.IntegerField(default=0),
        ),
    ]
