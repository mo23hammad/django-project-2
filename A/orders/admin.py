from django.contrib import admin
from .models import Order,OrderItem,Coupon

class OrderItemsInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ('product',)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user','paid','updated')
    list_filter = ('paid',)
    inlines = (OrderItemsInline,)

admin.site.register(Coupon)



