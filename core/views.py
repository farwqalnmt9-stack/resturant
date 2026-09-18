from django.contrib import messages
from django.shortcuts import render, redirect
from menu.models import Category, Product

def home(request): return render(request, 'core/home.html', {'categories':Category.objects.all(), 'featured':Product.objects.filter(featured=True, available=True)[:6]})
def contact(request):
    if request.method == 'POST':
        messages.success(request, 'شكراً لتواصلك معنا، سنرد عليك قريباً.')
        return redirect('core:contact')
    return render(request, 'core/contact.html')
