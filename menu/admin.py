from django.contrib import admin
from .models import Category, Extra, Product
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin): prepopulated_fields={'slug':('name',)}; list_display=('name','slug')
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin): list_display=('name','category','price','available','featured'); list_filter=('category','available','featured'); search_fields=('name','description'); prepopulated_fields={'slug':('name',)}; filter_horizontal=('extras',)
admin.site.register(Extra)

# Register your models here.
