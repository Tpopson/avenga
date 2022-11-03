from django.db import models

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=150)
    slug = models.SlugField(unique=True, null=False)
    video = models.FileField(upload_to='category', default='category/vid4.mp4')
    img = models.ImageField(upload_to = 'category-img', default = 'category-img/model6.jpg')

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'category'
        managed = True
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete= models.CASCADE)
    p_name = models.CharField(max_length= 150)
    slug = models.SlugField(unique=True, null=False)
    p_img = models.ImageField(upload_to = 'product', default = 'product/model7.jpg')
    p_price = models.IntegerField()
    p_des = models.TextField()
    p_min = models.IntegerField(default=1)
    p_max = models.IntegerField()

    def __str__(self):
        return self.p_name
    
    class Meta:
        db_table = 'product'
        managed = True
        verbose_name = 'Product'
        verbose_name_plural = 'Products'

    