Booking service API.

### start up project
```
docker-compose -f local.yml build
docker-compose -f local.yml up
```
### create superuser
```
 docker-compose -f local.yml run --rm django python manage.py createsuperuser
```
### load hall types
```
 docker-compose -f local.yml run --rm django python manage.py load_hall_type --file internal_files/hall_types.csv
```

## API
### Docs
1) http://127.0.0.1:8000/docs/
2) http://127.0.0.1:8000/redoc/

## Admin site
http://127.0.0.1:8000/admin
