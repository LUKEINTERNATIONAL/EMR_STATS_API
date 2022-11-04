run: python3 manage.py runserver
migrate: python3 manage.py migrate

first time you run the docker:
    python3 manage.py makemigrations
    python3 manage.py migrate
    python3 manage.py createsuperuser