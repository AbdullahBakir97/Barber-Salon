# Generated by Django 5.0.1 on 2024-02-16 01:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contact', '0012_owner_work_days_alter_message_message'),
    ]

    operations = [
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(choices=[('Stayling', 'Styling'), ('Massage', 'Massage'), ('Skin Care', 'Hautpflege')], default='Stayling', max_length=20, verbose_name='Kategorie')),
                ('service', models.CharField(choices=[('HairCut', 'Haarschnitt'), ('Beard', 'Bart'), ('Hair coloring', 'haare Färben'), ('Massage', 'Massage'), ('Maskes', 'Masken'), ('Stayling Products', 'Styling Produkte'), ('Skin Cleaning', 'Gesicht Reinigung')], default='HairCut', max_length=20, verbose_name='Service')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Preis')),
            ],
        ),
    ]
