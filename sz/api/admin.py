from sz.core.models import Category, Thing, Message
from django.contrib import admin

class CategoryAdmin(admin.ModelAdmin):
    list_per_page = 50
    ordering = ['name']

admin.site.register(Category, CategoryAdmin)

class ThingAdmin(admin.ModelAdmin):
    list_display = ('tag', 'stem')
    list_filter = ('category',)
    list_per_page = 50
    ordering = ['tag']

admin.site.register(Thing, ThingAdmin)

class MessageAdmin(admin.ModelAdmin):
    list_per_page = 50
    ordering = ['date']

admin.site.register(Message, MessageAdmin)