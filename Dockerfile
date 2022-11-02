FROM python:latest

RUN apt update
RUN apt install cron



COPY requirements.txt .
RUN pip install -r requirements.txt

RUN python manage.py crontab add

WORKDIR /app
CMD ["bash", "entry.sh"]
# CMD ["tail", "-f", "/dev/null"]
# python3 manage.py makemigrations