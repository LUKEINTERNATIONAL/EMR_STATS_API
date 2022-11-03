FROM python:latest

RUN apt update
RUN apt install -y cron

COPY requirements.txt .
RUN pip install -r requirements.txt

WORKDIR /app
ENTRYPOINT ["bash", "entry.sh"]
# CMD ["tail", "-f", "/dev/null"]