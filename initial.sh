# load hall types
python manage.py load_hall_type --file internal_files/hall_types.csv

# load type properties
python manage.py load_property_type --file internal_files/type_properties.csv

# load order status
python manage.py load_order_status --file internal_files/order_status.csv
