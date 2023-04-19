import pymongo
from django.db import models
from django.conf import settings

from users.models import User


class HallType(models.Model):
    type_name = models.CharField(max_length=120)

    def __repr__(self):
        return self.type_name

    def __str__(self):
        return self.type_name


class Hall(models.Model):
    """
    model represented hall
    """
    name = models.CharField(max_length=160, null=False)
    descriptions = models.TextField()
    moderated = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='halls', null=True, blank=True)
    hall_type = models.ManyToManyField(HallType, related_name='halls', blank=True)

    def __repr__(self):
        return self.name


class Property(models.Model):
    """
    all possible properties and related type
    """
    TYPES = (
        ('Boolean', 'bool'),
        ('String', 'str'),
        ('Integer', 'int'),
    )
    type = models.ForeignKey(HallType, on_delete=models.CASCADE, related_name='type_properties')
    property_name = models.CharField(max_length=160)
    property_type = models.CharField(choices=TYPES, max_length=20)

    def __repr__(self):
        return f'{self.property_name}({self.property_type})'

    def __str__(self):
        return f'{self.property_name}({self.property_type})'


client = pymongo.MongoClient(settings.MONGO_HOST, int(settings.MONGO_PORT))
db = client[settings.MONGO_DB]


class HallProperty(pymongo.collection.Collection):

    def __init__(self, hall_id, **kwargs):
        super().__init__(database=db, name='hall_properties', **kwargs)
        self.hall_id = hall_id
        self.properties = self.find_one({'hall_id': hall_id})

    def related_properties(self):
        properties = {}
        if self.properties is not None:
            properties = {key: value for key, value in self.properties.items() if key not in ['_id', 'hall_id']}
        return properties

    @classmethod
    def insert_properties(cls, hall_id, **kwargs):
        if hall_id is None:
            raise ValueError('Hall ID is required.')
        hall_property = cls(hall_id)
        properties = dict(kwargs)
        properties.pop('hall_id', None)  # Remove hall_id from properties
        hall_property.insert_one({'hall_id': hall_id, **properties})
        return hall_property

    def update_properties(self, **kwargs):
        kwargs.pop('hall_id', None)
        self.update_one(filter={'hall_id': self.hall_id}, update={"$set": {**kwargs}})
        self.properties = self.find_one({'hall_id': self.hall_id})
