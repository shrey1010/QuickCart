from django.db import models
from django.utils.text import slugify

# Create your models here.
class Category(models.Model):
    Category_name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=20,blank = True)


    def save(self , *args, **kwargs):
        self.slug = slugify(self.Category_name)
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.Category_name

class Product(models.Model):
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    product_name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='static/products/')
    stock = models.IntegerField(default=0)
    price = models.IntegerField(default=0,null=False)
    desc = models.TextField(blank=True)

    def __str__(self):
        return self.product_name

