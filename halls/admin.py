# from django.contrib import admin
#
# from halls.models import Hall, HallType, HallPropertyConferenceRoom, HallPropertyBanquetHall
#
#
# @admin.register(Hall)
# class HallAdmin(admin.ModelAdmin):
#     list_display = [
#         'name',
#         'latitude',
#         'longitude',
#         'descriptions',
#         'address',
#         'capacity',
#         'area',
#         'price',
#         'views_count',
#         'is_moderated'
#     ]
#     filter_horizontal = ('type',)
#
#
# @admin.register(HallType)
# class HallTypeAdmin(admin.ModelAdmin):
#     list_display = ['type_name']
#
#
# @admin.register(HallPropertyConferenceRoom)
# class HallPropertyConferenceRoomAdmin(admin.ModelAdmin):
#     using = 'mongo'
#     list_display = ['projector', 'whiteboard', 'speaker_system']