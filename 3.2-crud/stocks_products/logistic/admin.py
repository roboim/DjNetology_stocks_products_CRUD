from django.contrib import admin
from django.forms import BaseInlineFormSet

from logistic.models import Product, StockProduct, Stock


class RelationInline(admin.TabularInline):
    model = StockProduct
    formset = BaseInlineFormSet
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'description')
    list_filter = ('id', 'title')
    search_fields = ('id', 'title')
    inlines = [RelationInline]


@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ('id', 'address')
    list_filter = ('id', 'address')
    search_fields = ('id', 'address')
    inlines = [RelationInline]
