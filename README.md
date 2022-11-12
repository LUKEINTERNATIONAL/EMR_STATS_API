run: python3 manage.py runserver
migrate: python3 manage.py migrate

first time you run the docker:
    python3 manage.py makemigrations
    python3 manage.py migrate
    python3 manage.py createsuperuser

in server:
    make start
    make stop
    make restart SERVICE=[backend/frontend/nginx/db]

cronjob:
    */5 * * * * /usr/bin/python3 /var/www/EMR_STATS_API/manage.py crontab run bd9d26c4e133f356874ffa417534f010 >> /var/www/EMR_STATS_API/cronjob.log 2>&1

sudo psql --host=localhost --dbname=emr_stats --username=root