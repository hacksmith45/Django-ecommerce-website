# Generated by Django 4.2.1 on 2023-06-07 17:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0009_remove_cartorderitems_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cartorderitems',
            name='order',
        ),
        migrations.DeleteModel(
            name='CartOrder',
        ),
        migrations.DeleteModel(
            name='CartOrderItems',
        ),
    ]