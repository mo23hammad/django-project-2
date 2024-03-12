from django.db import models
from accounts.models import User
from home.models import Product

class Order(models.Model):
    user = models.ForeignKey(User,on_delete = models.CASCADE,related_name = 'uorders')
    paid = models.BooleanField(default = False)
    created = models.DateTimeField(auto_now_add = True)
    updated = models.DateTimeField(auto_now = True)
    discount = models.IntegerField(null = True,blank = True,default = None)

    class Meta:
        ordering = ('paid','-updated')
    
    def get_total_price(self):
        total = sum(float(item.get_cost()) for item in self.oitems.all())
        if self.discount:
            return format(total - (total/100)*self.discount,'.2f')
        return format(total,'.2f')
    def __str__(self):
        return f'{self.user} - {self.id}'

class OrderItem(models.Model):
    order = models.ForeignKey(Order,on_delete = models.CASCADE,related_name = 'oitems')
    product = models.ForeignKey(Product,on_delete = models.CASCADE,related_name = 'pitems')
    price = models.DecimalField(max_digits = 10,decimal_places = 2)
    quantity = models.IntegerField(default = 1)

    def get_cost(self):
        return format(self.price*self.quantity,'.2f')
    
    def __str__(self):
        return str(self.id)
    
class Coupon(models.Model):
    code = models.CharField(max_length = 20)
    discount = models.IntegerField()
    created = models.DateTimeField(auto_now_add = True)
    from_to = models.DateTimeField()
    expired = models.DateTimeField()
    active = models.BooleanField(default = True)

    def __str__(self):
        return str(self.code)
