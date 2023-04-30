import pymongo
from django.db import models
from django.conf import settings
from django.utils import timezone

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
    view_count = models.IntegerField(default=0)

    def __repr__(self):
        return self.name

    @property
    def properties(self):
        return HallProperty.get_hall_properties(hall_id=self.id)

    @property
    def approved_order_date(self):
        order_history = []
        orders = self.order.filter(histories__status__order_status_name='approved')
        for order in orders:
            order_history.append({'order_from': order.order_from, 'order_till': order.order_till})
        return order_history

    def delete(self, using=None, keep_parents=False):
        hall_id = self.id
        super(Hall, self).delete()
        HallProperty.delete_hall_record(hall_id=hall_id)

    def increase_view_count(self):
        self.view_count += 1
        self.save()


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


mongo_client = pymongo.MongoClient(settings.MONGO_HOST, int(settings.MONGO_PORT))
db = mongo_client[settings.MONGO_DB]


class HallProperty(pymongo.collection.Collection):

    def __init__(self, **kwargs):
        database = db
        super().__init__(database=database, name='hall_properties', **kwargs)

    @classmethod
    def get_hall_properties(cls, hall_id):
        properties = []
        hall_property = cls().find_one({'hall_id': hall_id})
        if hall_property is not None:
            for key, value in hall_property.items():
                if key not in ['_id', 'hall_id']:
                    properties.append({'property_name': key, 'property_value': value})
        return properties

    @classmethod
    def insert_properties(cls, hall_id, **kwargs):
        if hall_id is None:
            raise ValueError('Hall ID is required.')
        hall_property = cls()
        if hall_property.find_one({'hall_id': hall_id}) is not None:
            raise ValueError(f'Hall with hall_id {hall_id} already exists')
        properties = dict(kwargs)
        properties.pop('hall_id', None)  # Remove hall_id from properties
        hall_property.insert_one({'hall_id': hall_id, **properties})
        return hall_property

    @classmethod
    def update_properties(cls, hall_id, **kwargs):
        hall_property = cls()
        kwargs.pop('hall_id', None)
        hall_property.update_one(filter={'hall_id': hall_id}, update={"$set": {**kwargs}})

    @classmethod
    def delete_hall_record(cls, hall_id):
        hall_property = cls()
        hall_property.delete_one(filter={'hall_id': hall_id})

    @classmethod
    def all_properties(cls):
        cursor = cls().find({})
        return [doc for doc in cursor]
    @classmethod
    def delete_properties(cls, hall_id, **kwargs):
        hall_properties = cls()
        fields_for_delete = {key: "" for key in kwargs.keys()}
        hall_properties.update_one(filter={"hall_id": hall_id}, update={"$unset": {**fields_for_delete}})

