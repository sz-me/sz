from sz.core.models import Category, Thing, Message, Place
from django.contrib import admin
from django.contrib.gis import admin as gis_admin

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

from sz.core import services
def detect_things(modeladmin, request, queryset):
    things = Thing.objects.all()
    categorization = services.CategorizationService()
    [categorization.detect_things(things, message) for message in queryset]
detect_things.short_description = u"Определить вещи"

class MessageAdmin(admin.ModelAdmin):
    def things_to_str(self, obj):
        return ', '.join(map(lambda x: u'%s' % x, obj.things.all()))
    things_to_str.short_description = u'Вещи'
    list_display = ('date', 'user', 'text', 'place', 'things_to_str')
    list_display_links = ('text',)
    list_per_page = 25
    ordering = ['-date']
    actions = [detect_things]
    readonly_fields= ['things']

admin.site.register(Message, MessageAdmin)

class PlaceAdmin(gis_admin.OSMGeoAdmin):
    search_fields = ['name', 'address']
    list_display = ['name', 'address', 'position',]
    ordering = ['name']
    readonly_fields= ['id', 'date']

admin.site.register(Place, PlaceAdmin)