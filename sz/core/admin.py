from django.contrib import admin
from sz.core import models
from sz.core.services import morphology
from imagekit.admin import AdminThumbnail

categorization_service = morphology.CategorizationService(
    models.Category.objects.all(),
    morphology.RussianStemmingService())


class CategoryAdmin(admin.ModelAdmin):
    def things_to_str(self, obj):
        return ', '.join(map(lambda x: u'%s' % x, obj.thing_set.all()))
    things_to_str.short_description = u'Вещи'
    list_display = ('alias', 'name', 'keywords',)
    list_per_page = 50
    ordering = ('name',)

admin.site.register(models.Category, CategoryAdmin)

def index_message_text(model_admin, request, queryset):
    [categorization_service.assert_stems(message) for message in queryset]
index_message_text.short_description = u"Индексировать текст"


class MessageAdmin(admin.ModelAdmin):
    def categories_to_str(self, obj):
        return ', '.join(map(lambda x: u'%s' % x, obj.categories.all()))
    categories_to_str.short_description = u'Категории'

    def stems_to_str(self, obj):
        return ', '.join(map(lambda x: u'%s' % x, obj.stems.all().order_by('stem')))
    stems_to_str.short_description = u'Основы'

    admin_thumbnail = AdminThumbnail(image_field='thumbnail')
    list_display = ('date', 'user', 'text', 'admin_thumbnail', 'place',
                    'categories_to_str', 'stems_to_str')
    list_display_links = ('text',)
    list_filter = ('categories',)
    list_per_page = 25
    ordering = ('-date',)
    actions = (index_message_text,)
    readonly_fields = ('stems',)
    date_hierarchy = 'date'

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