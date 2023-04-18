from bson import ObjectId
from django.db import models
from djongo import models as mongo_model

from users.models import User


class CustomAutoField(models.AutoField):
    def db_type(self, connection):
        return 'ObjectId'

    def get_prep_value(self, value):
        if value is None:
            return ObjectId()
        return value


class Hall(models.Model):
    """
    model represented hall
    """
    name = models.CharField(max_length=160, null=False)
    descriptions = models.TextField()
    moderated = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='halls', null=True)

    def __repr__(self):
        return self.name

    def hall_properties(self):
        properties = {}
        hall_types = self.hall_types.values_list('type_name', flat=True)
        for hall_type in hall_types:
            hall_property = type_properties[hall_type].objects.filter(hall=self.id).values()[0]
            properties.update(hall_property)
        return properties

    class Meta:
        app_label = 'halls'
        managed = True


class HallType(models.Model):
    type_name = models.CharField(max_length=120)
    hall = models.ForeignKey(Hall, related_name='hall_types', on_delete=models.SET_NULL, null=True, blank=True)

    def __repr__(self):
        return self.type_name

    class Meta:
        app_label = 'halls'
        managed = True


class HallPropertyConferenceRoom(mongo_model.Model):
    """
    model represented properties of conference room
    """
    _id = mongo_model.AutoField(primary_key=True)
    hall = mongo_model.IntegerField()
    projector = mongo_model.BooleanField(default=False)
    whiteboard = mongo_model.BooleanField(default=False)
    speaker_system = mongo_model.BooleanField(default=False)

    class Meta:
        app_label = 'properties'
        db_table = 'halls_hallpropertyconferenceroom'


class Properties(models.Model):
    """
    all possible properties and related tyep
    """
    TYPES = {
        'Boolean': 'bool',
        'String': 'str',
        'Integer': 'int',
    }
    type = models.ForeignKey(HallType, on_delete=models.CASCADE, related_name='type_properties')
    property_name = models.CharField(max_length=160)
    property_type = models.CharField(choices=TYPES, max_length=20)


class HallPropertyMusicHall(mongo_model.Model):
    """
    model represented properties of music hall
    """
    _id = CustomAutoField(primary_key=True)
#     hall = mongo_model.IntegerField()
#     drum = mongo_model.BooleanField(default=False)
#     guitar = mongo_model.BooleanField(default=False)
#
    class Meta:
        app_label = 'properties'
        db_table = 'halls_hallpropertymusichall'
#
#
type_properties = {
    'conference_room': HallPropertyConferenceRoom,
    'music_hall': HallPropertyMusicHall,
}
