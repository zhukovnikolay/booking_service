Booking service API.

### start up project
```
docker-compose -f local.yml build
docker-compose -f local.yml up
```

### create superuser to use admin site

```
 docker-compose -f local.yml run --rm django python manage.py createsuperuser
```

### load reference book data
```
docker-compose -f local.yml run --rm django ./initial.sh
```

## API
### Docs
1) http://127.0.0.1:8000/docs/
2) http://127.0.0.1:8000/redoc/

## Admin site
http://127.0.0.1:8000/admin
