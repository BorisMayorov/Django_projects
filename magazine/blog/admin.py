from django.contrib import admin
from .models import *
from django.utils.safestring import mark_safe
# Register your models here.


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}


class PostAdmin(admin.ModelAdmin):

    # prepopulated_fields = {'slug': ('title',)}
    list_display = ('pk', 'title', 'slug', 'category',
                    'created_at', 'get_photo',)
    list_display_links = ('pk', 'title',)
    search_fields = ('title',)
    list_filter = ('category',)
    fields = ('title', 'content', 'get_photo', 'image', 'category',
              'created_at',)
    readonly_fields = ('created_at', 'get_photo',)
    # fieldsets = (
    #     (None, {'fields': ('title', 'image', 'content', 'category',), }),)

    save_as = True
    save_on_top = True

    def get_photo(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="50">')
        return '-'

    get_photo.short_description = 'image'


admin.site.register(Category, CategoryAdmin)
admin.site.register(Post, PostAdmin)
