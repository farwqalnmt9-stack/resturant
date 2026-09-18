from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render
from orders.models import Order
@login_required
def dashboard(request): return render(request,'delivery/dashboard.html',{'orders':Order.objects.filter(delivery_person=request.user).order_by('-created_at')})
@login_required
def order_map(request,number): return render(request,'delivery/map.html',{'order':get_object_or_404(Order,order_number=number,delivery_person=request.user)})
