from django.urls import path
from . import views
app_name='orders'
urlpatterns=[path('cart/',views.cart,name='cart'),path('cart/add/<int:product_id>/',views.add_to_cart,name='add'),path('cart/update/<int:product_id>/',views.update_cart,name='update'),path('checkout/',views.checkout,name='checkout'),path('success/<str:number>/',views.success,name='success'),path('my-orders/',views.my_orders,name='my_orders')]
