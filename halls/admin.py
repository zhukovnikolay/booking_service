from django.contrib import admin

from halls.models import Hall, HallType


@admin.register(Hall)
class HallAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'latitude',
        'longitude',
        'descriptions',
        'address',
        'capacity',
        'area',
        'price',
        'views_count',
        'is_moderated'
    ]
    filter_horizontal = ('type',)


@admin.register(HallType)
class HallTypeAdmin(admin.ModelAdmin):
    list_display = ['type_name']
