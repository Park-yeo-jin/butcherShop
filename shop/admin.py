from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import Category, Product, CategoryView

@admin.register(Category)
class CategoryAdmin(ModelAdmin):
    list_display = ('name', 'parent')
    search_fields = ('name',)


@admin.register(CategoryView)
class CategoryViewAdmin(ModelAdmin):
    list_display = ('name', 'parent')
    search_fields = ('name',)

    def get_queryset(self, request):

        return super().get_queryset(request).filter(categoryType='소분류')

@admin.register(Product)
class ProductAdmin(ModelAdmin):
    pass
    # list_display = ('name', 'content', 'stock', 'price', 'category', 'image')
    # search_fields = ('name',)
    # list_filter = ('category',)
