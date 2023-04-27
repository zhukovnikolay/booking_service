import random
from django.core.management import BaseCommand, CommandError

from halls.models import Hall, HallType, HallProperty


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('--hall-count', type=int, help='count of hall to create')

    def handle(self, *args, **options):
        hall_cnt_to_create = options['hall_count']
        all_hall_types = HallType.objects.all()
        while hall_cnt_to_create:
            hall_type_start = random.randint(0, all_hall_types.count() - 2)
            hall_type_end = random.randint(hall_type_start + 1, all_hall_types.count() - 1)
            hall_types = all_hall_types[hall_type_start:hall_type_end]
            hall = Hall.objects.create(
                name=f'test_hall_{hall_cnt_to_create}',
                descriptions=f'test_hall_{hall_cnt_to_create}',
                moderated=random.choice([True, False]),
            )
            hall.hall_type.add(*hall_types)
            hall_cnt_to_create -= 1
            new_property = {}
            for hall_type in hall_types:
                hall_type_properties = hall_type.type_properties.all()
                for hall_type_property in hall_type_properties:
                    if hall_type_property.property_type == 'int':
                        property_value = random.randint(100, 100000)
                    if hall_type_property.property_type == 'bool':
                        property_value = random.choice([True, False])
                    if hall_type_property.property_type == 'string':
                        property_value = f'some random string'
                    if hall_type_property.property_type == 'float':
                        property_value = round(random.random() * random.choice([10, 100, 1000, 10000]), 3)
                    new_property[hall_type_property.property_name] = property_value
            HallProperty().insert_properties(hall_id=hall.id, **new_property)

