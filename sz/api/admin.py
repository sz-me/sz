from sz.core.models import Tag, Pattern
from django.contrib import admin

class PatternInline(admin.StackedInline):
    model = Pattern
    extra = 1

class TagAdmin(admin.ModelAdmin):
    inlines = [PatternInline]
    list_per_page = 50
    ordering = ['name']
admin.site.register(Tag, TagAdmin)