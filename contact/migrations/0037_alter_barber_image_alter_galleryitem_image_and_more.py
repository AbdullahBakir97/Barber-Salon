# Generated by Django 5.0.1 on 2024-04-14 15:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contact', '0036_alter_barber_image_alter_galleryitem_image_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='barber',
            name='image',
            field=models.ImageField(upload_to='barber_images/', verbose_name='Foto'),
        ),
        migrations.AlterField(
            model_name='galleryitem',
            name='image',
            field=models.ImageField(upload_to='gallery_images/', verbose_name='Foto'),
        ),
        migrations.AlterField(
            model_name='owner',
            name='logo',
            field=models.ImageField(blank=True, null=True, upload_to='owner_logos/', verbose_name='Logo'),
        ),
        migrations.AlterField(
            model_name='review',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='review_images/', verbose_name='Foto'),
        ),
    ]
