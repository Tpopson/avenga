# Generated by Django 4.1.1 on 2022-10-04 10:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0009_alter_category_slug_alter_product_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='img',
            field=models.ImageField(default='category-img/model6.jpg', upload_to='category-img'),
        ),
        migrations.AlterField(
            model_name='product',
            name='p_img',
            field=models.ImageField(default='product/model7.jpg', upload_to='product'),
        ),
    ]