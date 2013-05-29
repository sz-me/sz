from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from django.utils.translation import ugettext_lazy as _
from imagekit.admin import AdminThumbnail

from .forms import UserChangeForm, UserCreationForm
from . import models
from .services import morphology


categorization_service = morphology.CategorizationService(
    models.Category.objects.all(),
    morphology.RussianStemmingService())


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('alias', 'name', 'description', 'keywords',)
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
    list_display = ('date', 'text', 'admin_thumbnail', 'place',
                    'categories_to_str', 'stems_to_str')
    list_display_links = ('date',)
    list_filter = ('categories',)
    list_per_page = 25
    ordering = ('-date',)
    actions = (index_message_text,)
    readonly_fields = ('stems',)
    date_hierarchy = 'date'

admin.site.register(models.Message, MessageAdmin)


class StyleAdmin(admin.ModelAdmin):
    list_display = ('name', 'description',)
    ordering = ('name',)

admin.site.register(models.Style, StyleAdmin)


class SmileAdmin(admin.ModelAdmin):
    list_display = ('style', 'emotion',)
    ordering = ('style',)

admin.site.register(models.Smile, SmileAdmin)


class SzUserAdmin(UserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('email', 'style', 'is_superuser')
    list_filter = ('is_superuser',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('style',)}),
        (_('Permissions'), {'fields': ('is_active', 'is_superuser')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'style', 'password1', 'password2')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()


admin.site.register(models.User, SzUserAdmin)
admin.site.unregister(Group)


class RegistrationProfileAdmin(admin.ModelAdmin):
    list_display = (
        'user', 'activation_key',
        'is_sending_email_required',
        'activation_key_expired'
    )

admin.site.register(models.RegistrationProfile, RegistrationProfileAdmin)

'''
from django.contrib.gis import admin as gis_admin
class PlaceAdmin(gis_admin.OSMGeoAdmin):
    search_fields = ['name', 'address']
    list_display = ['name', 'address', 'position',]
    ordering = ['name']
    readonly_fields= ['id', 'date']

admin.site.register(Place, PlaceAdmin)
'''
