from django.db.models import Q
from django.shortcuts import get_object_or_404, render
from .models import Category, Product

def product_list(request):
    products=Product.objects.filter(available=True).select_related('category'); q=request.GET.get('q',''); category=request.GET.get('category',''); order=request.GET.get('order','')
    if q: products=products.filter(Q(name__icontains=q)|Q(description__icontains=q))
    if category: products=products.filter(category__slug=category)
    if order in ('price','-price'): products=products.order_by(order)
    return render(request,'menu/list.html',{'products':products,'categories':Category.objects.all(),'q':q,'selected':category,'order':order})
def product_detail(request,slug): return render(request,'menu/detail.html',{'product':get_object_or_404(Product.objects.prefetch_related('extras'),slug=slug,available=True)})
