from sz.core import models
from django.contrib import admin
from imagekit.admin import AdminThumbnail

class CategoryAdmin(admin.ModelAdmin):
    def things_to_str(self, obj):
        return ', '.join(map(lambda x: u'%s' % x, obj.thing_set.all()))
    things_to_str.short_description = u'Вещи'
    list_display = ('alias','name', 'keywords',)
    list_per_page = 50
    ordering = ['name']

admin.site.register(models.Category, CategoryAdmin)


from sz.core import services
'''
def detect_things(modeladmin, request, queryset):
    things = models.Thing.objects.all()
    categorization = services.CategorizationService(things)
    [categorization.detect_things(message) for message in queryset]
detect_things.short_description = u"Развесить ярлычки"
'''

class MessageAdmin(admin.ModelAdmin):
    def categories_to_str(self, obj):
        return ', '.join(map(lambda x: u'%s' % x, obj.categories.all()))
    categories_to_str.short_description = u'Категории'
    admin_thumbnail = AdminThumbnail(image_field='thumbnail')
    list_display = ('date', 'user', 'text', 'admin_thumbnail', 'place',
                    'categories_to_str')
    list_display_links = ('text',)
    list_per_page = 25
    ordering = ['-date']
    #actions = [detect_things]
    #readonly_fields= ['things']

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