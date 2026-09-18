from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.db.models import Count, Sum
from django.shortcuts import redirect, render
from orders.models import Order
def login_view(request):
    form=AuthenticationForm(request,data=request.POST or None)
    if request.method=='POST' and form.is_valid(): login(request,form.get_user()); return redirect('core:home')
    return render(request,'accounts/auth.html',{'form':form,'mode':'تسجيل الدخول'})
def register(request):
    form=UserCreationForm(request.POST or None)
    if request.method=='POST' and form.is_valid(): login(request,form.save()); return redirect('core:home')
    return render(request,'accounts/auth.html',{'form':form,'mode':'إنشاء حساب'})
def logout_view(request): logout(request); return redirect('core:home')
@login_required
def profile(request):
    orders = request.user.orders.all()
    paid_orders = orders.filter(status=Order.Status.DELIVERED)
    stats = paid_orders.aggregate(total_spent=Sum('total'), delivered_count=Count('id'))
    return render(request, 'accounts/profile.html', {
        'order_count': orders.count(),
        'delivered_count': stats['delivered_count'] or 0,
        'total_spent': stats['total_spent'] or 0,
        'latest_orders': orders.order_by('-created_at')[:3],
    })
