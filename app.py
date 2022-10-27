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
import boto3
from botocore.exceptions import ClientError
import json
import db_creds

####


app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://lareb3:jonas@localhost/db_final"
url="postgresql://"+db_creds.username+":"+db_creds.password+"@"+db_creds.host+":"+db_creds.port+"/"+db_creds.db_name
app.config['SQLALCHEMY_DATABASE_URI'] =url

###

#app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://"+db_creds.username+":"+db_creds.password+"@"+db_creds.host+":"db_creds.port+"/"+db_creds.db_name

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

    def get_userinfo(self):
        return {feature.name: getattr(self, feature.name) for feature in self.__table__.columns}


class Document(db.Model):
    doc_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(100), nullable=False)
    user_id = db.Column(UUID(as_uuid=True), default=uuid.uuid4)
    #last_name = db.Column(db.String(100), nullable=False)
    #password = db.Column(db.String(100), nullable=False)
    #username = db.Column(db.String(20), unique=True, nullable=False)
    date_created = db.Column(db.DateTime, default = datetime.utcnow)
    s3_bucket_path = db.Column(db.String(100), nullable=False)
    

    
    def __repr__(self):
        return self.id
with app.app_context():
    db.create_all()
    db.session.commit()

class DocumentSchema(ma.Schema):
    class Meta:
        fields = ('doc_id', 'name', 'user_id' , 'date_created', 's3_bucket_path')

document_schema = DocumentSchema(many = False)
documents_schema = DocumentSchema(many = True)


# create student schema

class StudentSchema(ma.Schema):
    class Meta:
        fields = ('id', 'first_name', 'last_name', 'username', 'account_created','account_updated')

student_schema = StudentSchema(many = False)
students_schema = StudentSchema(many = True)

class CreateUser(Resource):
    def post(self):
        try:
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
        except:
            return "Bad request" , status.HTTP_400_BAD_REQUEST
        

@auth.verify_password
def verify_password(username, password):
    user = New_Student.query.filter_by(username=username).first()
    
    
    if(user and  bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8'))):
            return user.get_userinfo()
class GetAll(Resource):
    def get(self):
        new_students=New_Student.query.all()
        result_set = students_schema.dump(new_students)
        return jsonify(result_set)



class GetandPut(Resource):
    @auth.login_required
    def get(self,id):
        if(str(auth.current_user()['id'])!=id):

            return {"message":"Not authorized"} , 403
        else:
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
            if(len(data_update)==3):
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
            else:
                return "Record can not be updated" , status.HTTP_400_BAD_REQUEST


        except:
            return "Bad request" , status.HTTP_400_BAD_REQUEST
class Health(Resource):
    def get(self):
        return jsonify(response='200')


class UploadDocument(Resource):
    @auth.login_required
    def post(self):
        #if(str(auth.current_user()['id'])):
        user_id_variable=auth.current_user()['id']
            
        

        name = request.json['name']
        document_path = request.json['path']



        client = boto3.client("s3")
        try:
            print("I ma here")
            client.upload_file(document_path, "csye6225larebkhans3-dev", name)
            
            
            s3_path = "s3://csye6225larebkhans3-dev/"+name
            

            
            
            new_document = Document(name=name, user_id=user_id_variable, s3_bucket_path=s3_path)
            #new_document.metadata_db = x.ResponseMetadata
            db.session.add(new_document)
            db.session.commit()
            return make_response(document_schema.jsonify(new_document),201)
        
        except:
            print(ClientError)
            return "Bad request" , status.HTTP_400_BAD_REQUEST

    
    @auth.login_required
    def get(self):

        #document = Document.query.get_or_404(doc_id)
        #return document_schema.jsonify(document)
        #client = boto3.client("s3")
        #x=client.head_object(Bucket="csye6225larebkhans3-dev", Key="lareb1")
       
        #print(x)
        print('do')
        new_docs=(Document.query.filter_by(user_id=str(auth.current_user()['id'])))
        print('do',new_docs)
        result_set = documents_schema.dump(new_docs)
        return result_set
        
class GetDocument(Resource):

    @auth.login_required
    def get(self,doc_id):
        doc_details=Document.query.get(doc_id)
        if(doc_details and str(doc_details.user_id)!=str(auth.current_user()['id'])):
            
            return "Bad request" , 403
        try:
            
            return document_schema.jsonify(doc_details)

        except:
            return "Bad request" , 403
        
       
       



## delete 
    @auth.login_required
    def delete(self,doc_id):
        try:
            doc_details=Document.query.get(doc_id)
            if(doc_details and str(doc_details.user_id)!=str(auth.current_user()['id'])):
            
                return "Bad request" , 404
        
            name=doc_details.name
            
            client = boto3.client("s3")
            client.delete_object(Bucket='csye6225larebkhans3-dev', Key=name)
            db.session.delete(doc_details)
            db.session.commit()
            return "Done"
            
        except:
            return "Not found" , 404

# class GetAllDocument(Resource):
#     @auth.login_required
#     def get(self):

#         #document = Document.query.get_or_404(doc_id)
#         #return document_schema.jsonify(document)
#         #client = boto3.client("s3")
#         #x=client.head_object(Bucket="csye6225larebkhans3-dev", Key="lareb1")
       
#         #print(x)
#         print('do')
#         new_docs=(Document.query.filter_by(user_id=str(auth.current_user()['id'])))
#         print('do',new_docs)
#         result_set = documents_schema.dump(new_docs)
#         return result_set

class GetAllDocs(Resource):
    
    def get(self):
        new_docs=Document.query.all()
        result_set = documents_schema.dump(new_docs)
        return jsonify(result_set)

# class DeleteDocument(Resource):
#     @auth.login_required
#     def delete(self,doc_id):
#         document_delete = Document.query.get_or_404(doc_id)
#         name=document_delete.name

#         client = boto3.client("s3")
#         client.delete_object(Bucket='csye6225larebkhans3-dev', Key=name)
#         db.session.delete(document_delete)
#         db.session.commit()
#         return "Done"


api.add_resource(CreateUser, '/v1/account/')
api.add_resource(GetandPut, '/v1/account/<string:id>')   
api.add_resource(Health, '/healthz')
api.add_resource(GetAll, '/')
api.add_resource(UploadDocument, '/v1/documents')
api.add_resource(GetAllDocs, '/v1/alldocuments')
api.add_resource(GetDocument, '/v1/documents/<string:doc_id>')
#api.add_resource(DeleteDocument, '/v1/documents/<string:doc_id>')
        
if __name__ == "__main__":
    db.create_all()
    app.run(host = '0.0.0.0', port = 6000, debug = True)
