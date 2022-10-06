import os

from flask import Flask, request, url_for, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from sqlalchemy.sql import func
from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID
from flask_sqlalchemy import SQLAlchemy
import uuid
from flask_httpauth import HTTPBasicAuth
from flask import abort
from flask_api import status
import bcrypt
from flask import make_response
from flask_restful import Api, Resource


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://lareb3:jonas@localhost/db_final"

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


auth = HTTPBasicAuth()
ma = Marshmallow(app)
api = Api(app)
class New_Student(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(20), unique=True, nullable=False)
    account_created = db.Column(db.DateTime, default = datetime.utcnow)
    account_updated = db.Column(db.DateTime, default = datetime.utcnow)
    
    def __repr__(self):
        return self.id



# create student schema

class StudentSchema(ma.Schema):
    class Meta:
        fields = ('id', 'first_name', 'last_name', 'username', 'account_created','account_updated')

student_schema = StudentSchema(many = False)
students_schema = StudentSchema(many = True)

class CreateUser(Resource):
    def post(self):
        first_name = request.json['first_name']
        last_name = request.json['last_name']
        username = request.json['username']
        password_text=request.json['password']
    
    
        password_encoded=password_text.encode('utf-8')
        password = bcrypt.hashpw(password_encoded,bcrypt.gensalt())
        password_decoded=password.decode('utf-8')
    
        students = New_Student.query.all()
        for user in students:
            if(user.username==username):
                return "Record already exists" , status.HTTP_400_BAD_REQUEST

        new_student = New_Student(first_name = first_name, last_name = last_name, username = username, password=password_decoded)

        db.session.add(new_student)
        db.session.commit()
        return make_response(student_schema.jsonify(new_student),201)
        

@auth.verify_password
def verify_password(username, password):
    user = New_Student.query.filter_by(username=username).first()
    
    if(user and  bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8'))):
            return username
class GetAll(Resource):
    def get(self):
        new_students=New_Student.query.all()
        result_set = students_schema.dump(new_students)
        return jsonify(result_set)



class GetandPut(Resource):
    @auth.login_required
    def get(self,id):
        new_student = New_Student.query.get_or_404(id)
        return student_schema.jsonify(new_student)

    @auth.login_required
    def put(self,id):
    
        student_update = New_Student.query.get_or_404(id)
        data_update = request.get_json()
        required_keys=['first_name','last_name','password']


        if "username" in data_update.keys():
            return "Record can not be updated" , status.HTTP_400_BAD_REQUEST
        
        try:
            first_name = request.json['first_name']
            last_name = request.json['last_name']
            password_text=request.json['password']
    
    
            password_encoded=password_text.encode('utf-8')
            password = bcrypt.hashpw(password_encoded,bcrypt.gensalt())
            password_decoded=password.decode('utf-8')
            
    
            student_update.first_name=first_name
            student_update.last_name=last_name
            student_update.password=password_decoded
            student_update.account_updated = default = datetime.utcnow()
            db.session.commit()
            return make_response(student_schema.jsonify(student_update),204)

        except:
            return "Record can not be updated" , status.HTTP_400_BAD_REQUEST
class Health(Resource):
    def get(self):
        return jsonify(response='200')

api.add_resource(CreateUser, '/v1/account/')
api.add_resource(GetandPut, '/v1/account/<string:id>')   
api.add_resource(Health, '/healthz')
api.add_resource(GetAll, '/')
        
if __name__ == "__main__":
    app.run(port = 2000, debug = True)