# Generated by Django 4.2.1 on 2023-06-07 12:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_cart_coupon'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartitems',
            name='quantity',
            field=models.PositiveIntegerField(default=1),
        ),
    ]
