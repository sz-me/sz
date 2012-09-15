from sz.clothes.models import Tag, Pattern
from django.contrib import admin

class PatternInline(admin.StackedInline):
    model = Pattern
    extra = 1

class TagAdmin(admin.ModelAdmin):
    inlines = [PatternInline]

admin.site.register(Tag, TagAdmin)