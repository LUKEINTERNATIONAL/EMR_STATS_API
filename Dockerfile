FROM python:latest

COPY requirements.txt .
RUN pip install -r requirements.txt

WORKDIR /app
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
# CMD ["tail", "-f", "/dev/null"]
# python3 manage.py makemigrations