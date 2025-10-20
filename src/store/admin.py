from django.contrib import admin

from .models import Background, Category, Product


# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "slug"]
    prepopulated_fields = {
        "slug": ["name"],
    }


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "author",
        "slug",
        "price",
        "in_stock",
        "created",
        "updated",
    ]
    list_filter = ["in_stock", "is_active"]
    list_editable = ["in_stock", "price"]
    prepopulated_fields = {
        "slug": ["title"],
    }


@admin.register(Background)
class BackgroundAdmin(admin.ModelAdmin):
    list_display = ["title", "file_size"]
