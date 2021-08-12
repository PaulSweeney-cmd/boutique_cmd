from django.contrib import admin
from .models import Product, Category

# Register your models here.

# re-arranging the order of your products
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'sku',
        'name',
        'category',
        'price',
        'rating',
        'image',
    )
    ordering = ('sku',)


class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'friendly_name',
        'name',
    )

# registering models
admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
