#webapp

Prerequisites for building and deploying Flask

Python 3 and Flask


Assignment 1:
Building and deploying the flask app

flask run -p 3000


To check http status code
curl -v http://127.0.0.1:3000/healthz



To demo: 
mkdir newfolder
cd newfolder
git clone git@github.com:lareb-neu/webapp.git


Assignment 2: 

To demo: 
mkdir newfolder
cd newfolder
git clone git@github.com:lareb-neu/webapp.git

to run flask run -p 2000


The installation done:
pip3 install Flask Flask-SQLAlchemy
pip3 install Flask psycopg2-binary
Pip3 install marshmallow-sqlalchemy
Pip3 install flask-marshmallow
pip3 install flask-bcrypt
Pip3 install bcrypt
pip3 install Flask-HTTPAuth

python3
from app import db
 db.create_all()


New terminal
command line written down
flask shell
 from app import db

---------------

Run github actions  through merge and then everything will work and then enter command for cloud formation

Instance will be created and then runn all apis.


uploading to create AMi