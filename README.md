# install pip
sudo apt install python3-pip
# install env
sudo apt install python3-virtualenv
pip3 install virtualenv
# cd to project directory and create a project env using below command
virtualenv env
# TO activate env
source env/bin/activate
# install mysql package
sudo apt-get install libmysqlclient-dev
# Other dependace
sudo apt-get install libpq-dev
# install all requirements
pip install -r requirements.txt

# install postgres
sudo apt install postgresql postgresql-contrib
# To create user and database
sudo -u postgres psql
create database mydb;
create user myuser with encrypted password 'mypass';
grant all privileges on database mydb to myuser;
# migrations
python3 manage.py makemigrations
python3 manage.py migrate
# create user
python3 manage.py createsuperuser

# To start the application
python3 manage.py runserver
# for missing sessions
python manage.py migrate --fake sessions zero
python manage.py migrate sessions

# TO create load dump
pg_dump -U username -h localhost databasename > sqlfile.sql
# TO load dump
psql -h hostname -p port_number -U username -f your_file.sql databasename 

# Permission dennied during ping
To temporarily set this parameter, allowing all users to create ICMP sockets (until next boot):

sudo sysctl net.ipv4.ping_group_range='0 4294967295'
Some systems (e.g. Debian) may have issues with this, returning:

sysctl: setting key "net.ipv4.ping_group_range": Invalid argument
In this case, try:

sudo sysctl net.ipv4.ping_group_range='0   2147483647'

To permanently set this parameter:
echo "# allow all users to create icmp sockets\n net.ipv4.ping_group_range=0 2147483647" | sudo tee -a /etc/sysctl.d/ping_group.conf

# Install celery server
sudo apt-get install rabbitmq-server
# To create celery deamon 

1. The file that you have referred in the link https://github.com/celery/celery/blob/3.0/extra/generic-init.d/celeryd needs to be copied in your /etc/init.d folder with the name celeryd
2. Then you need to create a configuration file in the folder /etc/default with the name celeryd that is used by the above script. This configuration file basically defines certain variables and paths that are used by the above script. Here's an example configuration.
3. This link Generic init scripts explains the process and can be used for reference
