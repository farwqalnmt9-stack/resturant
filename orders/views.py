from decimal import Decimal
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from menu.models import Product
from .forms import CheckoutForm
from .models import Order, OrderItem

DELIVERY_FEE=Decimal('10000')
def _cart(request): return request.session.setdefault('cart',{})
def cart_data(request):
    cart=_cart(request); rows=[]; subtotal=Decimal('0')
    for key,item in cart.items():
        p=Product.objects.filter(pk=key,available=True).first()
        if p:
            qty=item['quantity']; line=p.price*qty; subtotal+=line
            rows.append({'product':p,'quantity':qty,'notes':item.get('notes',''),'extras':item.get('extras',[]),'line_total':line})
    return rows,subtotal
def add_to_cart(request,product_id):
    product=get_object_or_404(Product,pk=product_id,available=True)
    if request.method=='POST':
        cart=_cart(request); key=str(product.id); cart.setdefault(key,{'quantity':0,'notes':'','extras':[]}); cart[key]['quantity']+=max(1,int(request.POST.get('quantity',1))); cart[key]['notes']=request.POST.get('notes',''); cart[key]['extras']=request.POST.getlist('extras'); request.session.modified=True; messages.success(request,f'تمت إضافة {product.name} إلى السلة.'); return redirect('orders:cart')
    return redirect('menu:detail',slug=product.slug)
def update_cart(request,product_id):
    if request.method=='POST':
        cart=_cart(request); key=str(product_id); qty=int(request.POST.get('quantity',0))
        if qty>0 and key in cart: cart[key]['quantity']=qty
        else: cart.pop(key,None)
        request.session.modified=True
    return redirect('orders:cart')
def cart(request):
    rows,subtotal=cart_data(request); return render(request,'orders/cart.html',{'rows':rows,'subtotal':subtotal})
def checkout(request):
    rows,subtotal=cart_data(request)
    if not rows: messages.info(request,'سلتك فارغة.'); return redirect('menu:list')
    form=CheckoutForm(request.POST or None)
    if request.method=='POST' and form.is_valid():
        order=form.save(commit=False); order.customer=request.user if request.user.is_authenticated else None; order.payment_method='cash_on_delivery'; order.delivery_method=Order.Method.DELIVERY; order.subtotal=subtotal; order.delivery_fee=DELIVERY_FEE; order.total=order.subtotal+order.delivery_fee; order.save()
        for row in rows: OrderItem.objects.create(order=order,product=row['product'],product_name=row['product'].name,quantity=row['quantity'],price=row['product'].price,notes=row['notes'],extras=row['extras'])
        request.session['cart']={}; request.session.modified=True; return redirect('orders:success',number=order.order_number)
    return render(request,'orders/checkout.html',{'form':form,'rows':rows,'subtotal':subtotal,'delivery_fee':DELIVERY_FEE})
def success(request,number): return render(request,'orders/success.html',{'order':get_object_or_404(Order,order_number=number)})
@login_required
def my_orders(request): return render(request,'orders/my_orders.html',{'orders':request.user.orders.prefetch_related('items').order_by('-created_at')})
