
Install postgresSQL and configure database

python manage.py makemigrations

python manage.py migrate

python manage.py collectstatic

python manage.py createsuperuser

python manage.py runserver

Doc : API specifications accessible on those urls for those formats:


    JSON view: 127.0.0.1/swagger.json
    YAML view: 127.0.0.1/swagger.yaml
    Swagger-ui view: 127.0.0.1/swagger/
    ReDoc view: 127.0.0.1/redoc/
