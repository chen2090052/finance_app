from django.contrib import admin
from .models import Category, Transaction


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "type", "icon", "sort_order", "created_at"]
    list_filter = ["type", "is_deleted"]


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ["date", "type", "category", "amount", "note"]
    list_filter = ["type", "date", "is_deleted"]
