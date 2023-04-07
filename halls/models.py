from django.db import models


class HallType(models.Model):
    """
    reference book stored hall types
    """
    type_name = models.CharField(max_length=160)

    def __repr__(self):
        return self.type_name

    def __str__(self):
        return self.type_name


class Hall(models.Model):
    """
    model represented hall
    """
    name = models.CharField(max_length=160, null=False)
    latitude = models.FloatField()
    longitude = models.FloatField()
    descriptions = models.TextField()
    address = models.TextField(null=False, blank=False)
    capacity = models.IntegerField(null=False, blank=False)
    area = models.IntegerField(null=False, blank=False)
    type = models.ManyToManyField(HallType, related_name='hall_types')
    price = models.DecimalField(max_digits=50, decimal_places=2)
    views_count = models.IntegerField(default=0)
    is_moderated = models.BooleanField(default=False)

    def __repr__(self):
        return self.name

    def increment_views_count(self):
        self.name += 1
        self.save()


