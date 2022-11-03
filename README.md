run: python3 manage.py runserver
migrate: python3 manage.py migrate

first time you run the docker:
    python3 manage.py crontab add
    python3 manage.py makemigrations
    python3 manage.py migrate
    python3 manage.py createsuperuser
everytime you start the docker:
    cd /var/www/EMR_STATS_API/
    docker-compose run backend bash
    (in docker shell) cron