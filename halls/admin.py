from django.contrib import admin

from halls.models import Hall


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
        'type',
        'price',
        'vies_count',
    ]
