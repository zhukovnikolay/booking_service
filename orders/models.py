import datetime

from django.contrib.auth import get_user_model
from django.db import models

from halls.models import Hall


User = get_user_model()


class Order(models.Model):
    hall = models.OneToOneField(Hall, on_delete=models.CASCADE, related_name='order')
    order_from = models.DateTimeField()
    order_till = models.DateTimeField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    ordered_by = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, related_name='orders')


class OrderStatus(models.Model):
    order_status_name = models.CharField(max_length=120)

    def __repr__(self):
        return self.order_status_name

    def __str__(self):
        return self.order_status_name


class OrderHistory(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='histories')
    status = models.OneToOneField(OrderStatus, on_delete=models.SET_NULL, null=True)
    start_date = models.DateTimeField(null=True)
    end_date = models.DateTimeField(null=True)

    def save(self, *args, **kwargs):
        now = datetime.datetime.now(tz=datetime.timezone.utc)
        if not self.pk:
            previous_order = OrderHistory.objects.filter(order__id=self.order.id, end_date__isnull=True)
            if previous_order:
                previous_order.update(end_date=now)
                self.start_date = now
        super(OrderHistory, self).save(*args, **kwargs)
