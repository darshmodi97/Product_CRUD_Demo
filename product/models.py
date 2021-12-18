from django.db import models

# Create your models here.
from taggit.managers import TaggableManager


class TimeStampModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Category(TimeStampModel):
    name = models.CharField(max_length=256)
    parent = models.ForeignKey("self", blank=True, null=True, verbose_name='category', on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Product(TimeStampModel):
    name = models.CharField(max_length=512, verbose_name='Product name')
    tags = TaggableManager(verbose_name="Tags", related_name="product_tags")
    image = models.ImageField(upload_to='image/', blank=True, null=True)
    category = models.ForeignKey(Category, related_name="products", blank=True, null=True, on_delete=models.SET_NULL)
    description = models.TextField()

    def __str__(self):
        return self.name
