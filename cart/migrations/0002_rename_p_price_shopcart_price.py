# Generated by Django 4.1.1 on 2022-10-18 11:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='shopcart',
            old_name='p_price',
            new_name='price',
        ),
    ]
