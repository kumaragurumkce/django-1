# Generated by Django 4.2.14 on 2024-08-07 06:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0002_contact'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='out_of_stock',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='product',
            name='quantity',
            field=models.PositiveIntegerField(default=0),
        ),
    ]