from django.db import models
from django.urls import reverse

class Category(models.Model):
    name = models.CharField(max_length = 200)
    slug = models.SlugField(max_length = 200,unique = True)
    is_sub = models.BooleanField(default = False)
    sub_category = models.ForeignKey('self',on_delete = models.CASCADE,related_name = 'scategory',null = True,blank = True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'
    
    def __str__(self):
        return self.slug
    
    def get_absolute_url(self):
        return reverse('home:category_filter', args=[self.slug,])

class Product(models.Model):
    category = models.ManyToManyField(Category)
    name = models.CharField(max_length = 200)
    slug = models.SlugField(max_length = 200,unique = True)
    image = models.ImageField(null=True,blank = True)
    price = models.DecimalField(max_digits = 10 , decimal_places = 2)
    available = models.BooleanField(default = True)
    description = models.TextField()
    created = models.DateTimeField(auto_now_add = True)
    updated = models.DateTimeField(auto_now = True)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name
    def get_absolute_url(self):
        return reverse('home:product_detail',args=[self.slug,])
    