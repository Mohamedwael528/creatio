# Generated by Django 5.0.6 on 2024-06-14 08:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0002_product_firist_image_product_main_images_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='main_images',
            new_name='main_image',
        ),
    ]
