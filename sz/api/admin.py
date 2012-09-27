from sz.core.models import DomainTag, DomainPattern
from django.contrib import admin

class DomainPatternInline(admin.StackedInline):
    model = DomainPattern
    extra = 1

class DomainTagAdmin(admin.ModelAdmin):
    inlines = [DomainPatternInline]
    list_per_page = 50
    ordering = ['name']

admin.site.register(DomainTag, DomainTagAdmin)