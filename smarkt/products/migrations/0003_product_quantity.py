# Generated by Django 2.0.3 on 2018-03-15 17:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_product_average_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='quantity',
            field=models.IntegerField(blank=True, default=0),
        ),
    ]
