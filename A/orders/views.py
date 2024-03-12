from django.shortcuts import render,get_object_or_404,redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .cart import Cart
from home.models import Product
from .forms import AddCartForm,CouponForm
from .models import Order,OrderItem,Coupon
from datetime import datetime
from django.contrib import messages

class CartView(View):
    def get(self,request):
        cart = Cart(request)
        return render(request,'orders/cart.html',{'cart':cart})
    
class AddCartView(View):

    def post(self,request,product_id):
        product = get_object_or_404(Product,id = product_id)
        cart = Cart(request)
        form = AddCartForm(request.POST)
        if form.is_valid():
            cart.add(product,form.cleaned_data['quantity'])
        return redirect('orders:cart')

class RemoveCartView(View):
    def get(self,request,product_id):
        cart = Cart(request)
        cart.remove(str(product_id))
        return redirect('orders:cart')
    
class OrderDetailView(LoginRequiredMixin,View):
    def get(self,request,order_id):
        order = get_object_or_404(Order,id = order_id)
        form = CouponForm()
        return render(request,'orders/order.html',{'order':order,'form':form})
    def post(self,request,order_id):
        form = CouponForm()
        order = get_object_or_404(Order,id = order_id)
        now = datetime.now()
        if form.is_valid():
            try:
                coupon = Coupon.objects.get(code__exact = form.cleaned_data['code'],from_to__lte = now,expired__gte = now,active = True)
                order.discount = coupon.discount
                order.save()
            except Coupon.DoesNotExist:
                messages.error(request,'this code does not exists')
        return redirect('orders:order_detail',order.id)
            
    
class OrderCreateView(LoginRequiredMixin,View):
    def get(self,request):
        order = Order.objects.create(user = request.user)
        cart = Cart(request)
        for item in cart:
            OrderItem.objects.create(order = order,product = item['product'],price = float(item['price']),quantity = item['quantity'])
        cart.clear()
        return redirect('orders:order_detail',order.id)
        




