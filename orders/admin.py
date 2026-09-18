from django.contrib import admin
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Count, Sum
from django.shortcuts import render
from django.utils.dateparse import parse_date
from django.utils import timezone
from django.utils.html import format_html
from urllib.parse import quote
from .models import Order, OrderItem


@staff_member_required
def revenue_report(request):
    """Revenue report for completed (delivered) cash-on-delivery orders."""
    today = timezone.localdate()
    start_date = parse_date(request.GET.get('start', '')) or today
    end_date = parse_date(request.GET.get('end', '')) or today
    invalid_range = start_date > end_date
    completed_orders = Order.objects.none() if invalid_range else Order.objects.filter(
        status=Order.Status.DELIVERED,
        created_at__date__range=(start_date, end_date),
    )
    totals = completed_orders.aggregate(revenue=Sum('total'), orders_count=Count('id'))
    context = {
        **admin.site.each_context(request),
        'title': 'تقرير الإيرادات',
        'start_date': start_date,
        'end_date': end_date,
        'invalid_range': invalid_range,
        'revenue': totals['revenue'] or 0,
        'orders_count': totals['orders_count'] or 0,
        'orders': completed_orders.order_by('-created_at'),
    }
    return render(request, 'admin/revenue_report.html', context)


class OrderItemInline(admin.TabularInline): model=OrderItem; extra=0; readonly_fields=('product_name','quantity','price','notes','extras')
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display=('order_number','customer_name','phone','total','delivery_method','status','created_at','map_link','whatsapp_confirmation'); list_filter=('status','delivery_method','created_at'); search_fields=('order_number','customer_name','phone'); inlines=[OrderItemInline]
    def map_link(self,obj):
        if obj.delivery_latitude and obj.delivery_longitude: return format_html('<a target="_blank" href="https://www.openstreetmap.org/?mlat={}&mlon={}#map=17/{}/{}">فتح الموقع</a>',obj.delivery_latitude,obj.delivery_longitude,obj.delivery_latitude,obj.delivery_longitude)
        return '—'
    map_link.short_description='موقع العميل'

    def whatsapp_confirmation(self, obj):
        """Open WhatsApp with a ready-to-send order confirmation message."""
        phone = ''.join(char for char in obj.phone if char.isdigit())
        if phone.startswith('0'):
            phone = f'963{phone[1:]}'
        if not phone:
            return '—'
        message = quote(f'أهلًا، تم استلام طلبك رقم #{obj.order_number} من سُفرة حلب. سنبدأ تحضيره قريبًا.')
        return format_html('<a target="_blank" href="https://wa.me/{}?text={}">تأكيد عبر واتساب</a>', phone, message)
    whatsapp_confirmation.short_description = 'واتساب'

# Register your models here.
