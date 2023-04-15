from django.db import models
from djongo import models as mongo_model


class HallType(models.Model):
    type_names = models.CharField(max_length=120)

    class Meta:
        app_label = 'halls'
        managed = True


class Hall(models.Model):
    """
    model represented hall
    """
    name = models.CharField(max_length=160, null=False)
    descriptions = models.TextField()
    hall_type = models.ForeignKey(HallType, related_name='halls', on_delete=models.SET_NULL, null=True, blank=True)

    def __repr__(self):
        return self.name

    class Meta:
        app_label = 'halls'
        managed = True


class HallPropertyConferenceRoomMongoDB(mongo_model.Model):
    """
    model represented properties of conference room
    """
    hall_id = mongo_model.IntegerField()
    projector = mongo_model.BooleanField(default=False)
    whiteboard = mongo_model.BooleanField(default=False)
    speaker_system = mongo_model.BooleanField(default=False)

    class Meta:
        app_label = 'properties'
        db_table = 'halls_hallpropertyconferenceroommongodb'

