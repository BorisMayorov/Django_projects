from django.contrib import admin
from django.utils.safestring import mark_safe

# Register your models here.

from .models import *


class PostAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    save_as = True
    fields = ('name', 'slug', 'content', 'picture', 'get_picture',
              'category', 'tags', 'author',)
    readonly_fields = ('views', 'get_picture')
    list_display = ('pk', 'name', 'slug', 'category',
                    'author', 'created_at', 'get_picture')
    list_display_links = ('pk', 'name')
    search_fields = ('name',)
    list_filter = ('category',)
    save_on_top = True

    def get_picture(self, obj):
        if obj.picture:
            return mark_safe(f'<img src="{obj.picture.url}" width="50">')
        return '---'
    get_picture.short_description = 'Picture'


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('pk', 'name', 'slug',)
    list_display_links = ('pk', 'name')


class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('pk', 'name', 'slug',)
    list_display_links = ('pk', 'name',)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'created', 'active',)
    list_filter = ('user', 'created', 'updated', 'active',)
    search_fields = ('user', 'post', 'body',)
    list_display_links = ('user', 'post',)


admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
