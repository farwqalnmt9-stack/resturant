import uuid
from django.conf import settings
from django.db import models
from menu.models import Product


class Order(models.Model):
    class Method(models.TextChoices): PICKUP='pickup','استلام من المطعم'; DELIVERY='delivery','توصيل'
    class Status(models.TextChoices): PENDING='pending','قيد الانتظار'; CONFIRMED='confirmed','تم التأكيد'; PREPARING='preparing','قيد التحضير'; READY='ready','جاهز'; OUT='out','في الطريق'; DELIVERED='delivered','تم التسليم'; CANCELLED='cancelled','ملغى'
    order_number = models.CharField(max_length=12, unique=True, editable=False)
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL, related_name='orders')
    customer_name = models.CharField(max_length=120, blank=True); phone = models.CharField(max_length=30); extra_phone = models.CharField(max_length=30, blank=True)
    delivery_address = models.TextField(blank=True)
    neighborhood = models.CharField(max_length=100, blank=True); street = models.CharField(max_length=120, blank=True); building = models.CharField(max_length=120, blank=True); floor = models.CharField(max_length=30, blank=True); landmark = models.CharField(max_length=160, blank=True)
    delivery_latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True); delivery_longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2); delivery_fee = models.DecimalField(max_digits=8, decimal_places=2, default=0); total = models.DecimalField(max_digits=10, decimal_places=2)
    notes = models.TextField(blank=True); delivery_method = models.CharField(max_length=12, choices=Method.choices); payment_method = models.CharField(max_length=30, default='cash_on_delivery', editable=False); status = models.CharField(max_length=16, choices=Status.choices, default=Status.PENDING)
    delivery_person = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL, related_name='delivery_orders')
    created_at = models.DateTimeField(auto_now_add=True); updated_at = models.DateTimeField(auto_now=True)
    def save(self, *args, **kwargs):
        if not self.order_number: self.order_number = uuid.uuid4().hex[:10].upper()
        super().save(*args, **kwargs)
    @property
    def address(self): return self.delivery_address or '، '.join(x for x in [self.neighborhood, self.street, self.building, self.floor, self.landmark] if x)
    def __str__(self): return f'#{self.order_number}'


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items'); product = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL)
    product_name = models.CharField(max_length=140); quantity = models.PositiveIntegerField(); price = models.DecimalField(max_digits=8, decimal_places=2); notes = models.CharField(max_length=250, blank=True); extras = models.JSONField(default=list, blank=True)
    @property
    def line_total(self): return self.price * self.quantity
