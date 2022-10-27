#!/bin/bash
#updating the package manager
sleep 20
sudo apt-get update

sudo apt-get install zip unzip

sudo apt-get install python3 -y
sudo apt install python3-pip -y
sudo apt install gunicorn3 -y
sudo apt-get install nginx -y
#installing python, gunicorn and nginx to run and deploy the web api
#sudo apt-get install python3 -y
#sudo apt install python3-pip -y
#installing nginx and gunicorn
#sudo apt install gunicorn3 -y
#sudo apt-get install nginx -y

#echo "Installing postgresql server"
#sudo apt-get install postgresql postgresql-contrib -y

#unzipping the file and copying it's contents to ubuntu machine
#sudo apt-get install zip unzip
cd ~/ && unzip webapp_local.zip
#installing required libraries
cd /home/ubuntu/webapp_local
sudo pip3 install flask
sudo pip3 install flask_restful
sudo pip3 install bcrypt
sudo pip3 install psycopg2-binary
sudo pip3 install flask_api
sudo pip3 install Datetime
sudo pip3 install SQLAlchemy
sudo pip3 install flask-marshmallow
sudo pip3 install Flask-HTTPAuth
sudo pip3 install flask-sqlalchemy
sudo pip3 install boto3

#installing posgtrssql and creating database


#echo "creating data base"
#sudo -iu postgres psql <<EOF

#CREATE DATABASE db_final;

#CREATE USER lareb3 WITH PASSWORD 'jonas';

#GRANT ALL PRIVILEGES ON DATABASE db_final TO lareb3;
#EOF

#echo "Starting postgresql server"


#copying the files for nginx and gunicorn service 
sudo cp /home/ubuntu/webapp_local/gunicorn.service /etc/systemd/system/gunicorn.service
sudo cp /home/ubuntu/webapp_local/network_file /etc/nginx/sites-available/default

#satrting the services

#sudo service postgresql start

#echo "Starting gunicorn server"
#sudo systemctl daemon-reload
#sudo systemctl start gunicorn
#sudo systemctl enable gunicorn

#echo "Starting nginx server"
#sudo systemctl start nginx
#sudo systemctl enable nginx
#echo "Script executed successfully"


