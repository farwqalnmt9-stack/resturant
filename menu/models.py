from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=80, unique=True)
    slug = models.SlugField(unique=True, allow_unicode=True)
    image = models.ImageField(upload_to='categories/', blank=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self): return self.name


class Extra(models.Model):
    name = models.CharField(max_length=80)
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    def __str__(self): return self.name


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='products')
    name = models.CharField(max_length=140)
    slug = models.SlugField(unique=True, allow_unicode=True)
    description = models.TextField()
    image = models.ImageField(upload_to='products/', blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    available = models.BooleanField(default=True)
    featured = models.BooleanField(default=False)
    extras = models.ManyToManyField(Extra, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self): return self.name
