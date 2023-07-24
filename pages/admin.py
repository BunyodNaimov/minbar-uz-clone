from django.contrib import admin

from pages.models import Page, Post, Position


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = ('name',)
    prepopulated_fields = {
        "slug": ('name',)
    }


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    list_display = ('name', 'author')
    prepopulated_fields = {
        "slug": ('name',)
    }


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'page')
    prepopulated_fields = {
        "slug": ('title',)
    }
