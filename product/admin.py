from django.contrib import admin

# Register your models here.
from product.models import Category, Product


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'parent']


class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'tags', 'image', 'category', 'description']


admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
