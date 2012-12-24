from sz.core import models
from django.contrib import admin

class CategoryAdmin(admin.ModelAdmin):
    def things_to_str(self, obj):
        return ', '.join(map(lambda x: u'%s' % x, obj.thing_set.all()))
    things_to_str.short_description = u'Вещи'
    list_display = ('name', 'body_part', 'gender', 'layer', 'things_to_str',)
    list_filter = ('body_part', 'gender', 'layer',)
    list_per_page = 50
    ordering = ['name']

admin.site.register(models.Category, CategoryAdmin)

class ThingAdmin(admin.ModelAdmin):
    list_display = ('name', 'stem', 'category',)
    list_filter = ('category',)
    list_per_page = 50
    ordering = ['name']

admin.site.register(models.Thing, ThingAdmin)

from sz.core import services
def detect_things(modeladmin, request, queryset):
    things = models.Thing.objects.all()
    categorization = services.CategorizationService()
    [categorization.detect_things(things, message) for message in queryset]
detect_things.short_description = u"Развесить ярлычки"

class MessageAdmin(admin.ModelAdmin):
    def things_to_str(self, obj):
        return ', '.join(map(lambda x: u'%s' % x, obj.things.all()))
    things_to_str.short_description = u'Вещи'
    def categories_to_str(self, obj):
        tags = set(['%s' % thing.category for thing in obj.things.all()])
        return ', '.join(tags)
    categories_to_str.short_description = u'Категории'
    list_display = ('date', 'user', 'text', 'place',
                    'things_to_str', 'categories_to_str')
    list_display_links = ('text',)
    list_per_page = 25
    ordering = ['-date']
    actions = [detect_things]
    readonly_fields= ['things']

admin.site.register(models.Message, MessageAdmin)
'''
from django.contrib.gis import admin as gis_admin
class PlaceAdmin(gis_admin.OSMGeoAdmin):
    search_fields = ['name', 'address']
    list_display = ['name', 'address', 'position',]
    ordering = ['name']
    readonly_fields= ['id', 'date']

admin.site.register(Place, PlaceAdmin)
'''