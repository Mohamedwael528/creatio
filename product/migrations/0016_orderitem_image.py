# Generated by Django 5.0.6 on 2024-06-16 08:35

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0015_remove_orderitem_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='image',
            field=models.ImageField(default=django.utils.timezone.now, upload_to='photos/'),
        ),
    ]
