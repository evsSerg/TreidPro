from django.contrib import admin

from .models import Category, InfoPage, MenuItem, NewsArticle, Product, Promotion


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'page_type', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    ordering = ('order',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'stock', 'is_featured', 'is_recommended')
    list_filter = ('category', 'is_featured', 'is_recommended')
    search_fields = ('name', 'short_description', 'description')
    list_editable = ('price', 'stock', 'is_featured', 'is_recommended')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(InfoPage)
class InfoPageAdmin(admin.ModelAdmin):
    list_display = ('title', 'page_type')


@admin.register(NewsArticle)
class NewsArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'published_at', 'is_published')
    list_filter = ('is_published', 'published_at')
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Promotion)
class PromotionAdmin(admin.ModelAdmin):
    list_display = ('title', 'discount_label', 'created_at', 'is_published')
    list_filter = ('is_published', 'created_at')
    prepopulated_fields = {'slug': ('title',)}
