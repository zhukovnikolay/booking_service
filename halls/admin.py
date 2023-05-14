from django.contrib import admin

from halls.models import Hall, HallType, Property


@admin.register(Hall)
class HallAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'descriptions',
        'moderated',
        'owner',
    ]

    filter_horizontal = ('hall_type',)


@admin.register(HallType)
class HallTypeAdmin(admin.ModelAdmin):
    list_display = ['type_name', ]


@admin.register(Property)
class HallPropertyConferenceRoomAdmin(admin.ModelAdmin):
    list_display = ['hall_type', 'property_name', 'property_type' ,]
