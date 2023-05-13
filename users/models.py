from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):

    email = models.EmailField(blank=False)
    first_name = models.CharField(max_length=120, blank=False, null=False)
    last_name = models.CharField(max_length=120, blank=False, null=False)
    user_agreement = models.BooleanField(default=True, blank=False)
    offer_agreement = models.BooleanField(default=True, blank=False)
    show_phone_number = models.BooleanField(default=True, blank=False)
    phone_number = models.CharField(max_length=12, null=True)
