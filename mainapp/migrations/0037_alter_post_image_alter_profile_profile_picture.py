# Generated by Django 4.0.5 on 2022-06-29 14:21

import django.core.validators
from django.db import migrations, models
import mainapp.validators


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0036_alter_post_image_alter_profile_profile_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='images/', validators=[mainapp.validators.validate_file_size, django.core.validators.FileExtensionValidator(allowed_extensions=['jpg', 'jpeg'])]),
        ),
        migrations.AlterField(
            model_name='profile',
            name='profile_picture',
            field=models.ImageField(blank=True, null=True, upload_to='images/', validators=[mainapp.validators.validate_file_size, django.core.validators.FileExtensionValidator(allowed_extensions=['jpg', 'jpeg'])]),
        ),
    ]
