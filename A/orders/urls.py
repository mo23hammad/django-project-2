from django.urls import path
from . import views

app_name = 'orders'
urlpatterns = [
    path('order/detail/<order_id>/',views.OrderDetailView.as_view(),name = 'order_detail'),
    path('order/create/',views.OrderCreateView.as_view(),name = 'order_create'),
    path('cart/',views.CartView.as_view(),name = 'cart'),
    path('cart/add/<int:product_id>/',views.AddCartView.as_view(),name = 'add_cart'),
    path('cart/remove/<int:product_id>/',views.RemoveCartView.as_view(),name = 'remove_cart'),
]
