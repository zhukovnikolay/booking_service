import random
from datetime import timedelta
from django.core.management import BaseCommand
from django.utils import timezone

from halls.models import Hall
from orders.models import OrderStatus


class Command(BaseCommand):

    def handle(self, *args, **options):
        halls = Hall.objects.all()
        hall_from = random.randint(0, halls.count()-1)
        hall_to = random.randint(hall_from, halls.count()-1)
        halls_to_create_order = halls[hall_from:hall_to]
        for hall in halls_to_create_order:
            order_count = random.randint(0, 10)
            while order_count:
                if not hall.order.count():
                    order_from = timezone.now()
                else:
                    order_from = hall.order.latest('order_from').order_from + timedelta(days=random.randint(1, 30))
                order = hall.order.create(order_from=order_from,
                                          order_till=order_from + timedelta(days=random.randint(1, 3)),
                                          price=random.random() * random.randint(1000, 3000)
                                          )
                order.histories.create(
                    status=random.choice(OrderStatus.objects.all()),
                    start_date=order_from
                                       )
                order_count -= 1
