import random

from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('--count', type=int, help='count of user to create')

    def handle(self, *args, **options):
        user_count = options['count']
        while user_count:
            show_phone_number = bool(random.random() * random.randint(0, 1))
            username = f'test_user_{user_count * random.randint(15 ,90)}'
            User.objects.create(
                username=username,
                email=f'{username}@google.com',
                first_name='test',
                last_name='test',
                show_phone_number=show_phone_number,
                phone_number=int(random.random() * 1000000000000),
                is_active=True
            )
            user_count -= 1
