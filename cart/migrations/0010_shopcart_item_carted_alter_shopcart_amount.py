# Generated by Django 4.1.1 on 2022-11-08 12:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0009_alter_shipping_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='shopcart',
            name='item_carted',
            field=models.IntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='shopcart',
            name='amount',
            field=models.FloatField(),
        ),
    ]
