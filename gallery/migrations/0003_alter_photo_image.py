# Generated by Django 4.1.7 on 2023-05-14 10:34

from django.db import migrations, models
import gallery.models


class Migration(migrations.Migration):

    dependencies = [
        ("gallery", "0002_alter_photo_photo_category"),
    ]

    operations = [
        migrations.AlterField(
            model_name="photo",
            name="image",
            field=models.ImageField(
                blank=True, null=True, upload_to=gallery.models.photo_image_upload_path
            ),
        ),
    ]
