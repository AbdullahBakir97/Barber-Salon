# Generated by Django 5.0.1 on 2024-04-14 14:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0013_alter_ownerprofile_owner_alter_ownerprofile_user_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ownerprofile',
            name='image',
            field=models.ImageField(upload_to='static/profile_images/', verbose_name='Foto'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='profile_image',
            field=models.ImageField(blank=True, null=True, upload_to='static/profile_images/', verbose_name='Profile Foto'),
        ),
    ]
