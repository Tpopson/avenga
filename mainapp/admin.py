from django.contrib import admin
from .models import *
# Register your models here.

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id','name','slug', 'video','img')
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['img']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id','category','p_name','slug', 'p_img', 'p_price','p_des','p_min','p_max')
    prepopulated_fields = {'slug': ('p_name',)}
