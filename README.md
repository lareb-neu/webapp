# Flask_app_deployed_to_AWS_using_AMI


---------------------------------------------------------------

### Summary

This is a RESTful APIs based web application that allowed users to register themselves and upload thier files in any format to s3 bucket built with Flask, PostgreSQL, and deployed on AWS

-   EC2 instances are built on a custom
    [AMI](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/AMIs.html)
    using [packer](https://packer.io/)
-   Setting up the network and creation of resources is automated with
    Cloud formation, aws cli and shell scripts
-   Instances are autoscaled with
    [ELB](https://aws.amazon.com/elasticloadbalancing/) to handle the
    web traffic
-   Created a [serverless](https://aws.amazon.com/lambda/) application
    to send a mail to user once he registers.
    [SES](https://aws.amazon.com/ses/) and
    [SNS](https://aws.amazon.com/sns/)
-   The application is automaticaly tested using pytest and deployed using Github workflow once the pull request is merged.

### Architecture Diagram

 ![aws_full](https://user-images.githubusercontent.com/42703011/92800898-211c7580-f383-11ea-9b4e-76c171fca750.png)


Tools and Technologies
----------------------
                          
| Infrastructure       | VPC, ELB, EC2, Route53, Cloud formation, Shell, Packer |
|----------------------|--------------------------------------------------------|
| Webapp               | Python, Flask, PostgreSQL, DynamoDB                    |
| CI/CD                | Github Worflow                                         |
| Alerting and logging | statsd, Cloud Watch, SNS, SES, Lambda                  |
| Security             | KMS and EBS for encryption of RDS and  EC2, and SSL certificate for domain name using Route53 and DNS.   |
                      


Infrastructure-setup
--------------------

-   Create the networking setup using AWS CloudFormation and AWS CLI
-   Create the required IAM policies and users
-   Setup Load Balancers, Route53, DynamoDB, SNS, SES, RDS

Webapp
------

-   The Web application is developed using
    Flask framework that uses the REST architecture
-   Secured the application with Basic
    [authentication](https://developer.mozilla.org/en-US/docs/Web/HTTP/Authentication)
    to retrieve user information
-   Storing the files uplaoded by users in S3 bucket and retrieving as an object.
-   Generating [verification URL] with expiration of 3 minutes using DynamoDB


## Build Instructions
Pre-Requisites: Need to have postman installed
-  Clone this repository  into the local system 
-  Go to the folder Flask_app_deployed_to_AWS_using_AMI /webapp
-  Download all the packages listed in requirements.txt using pip
-  Run WebappApplication in your local server by running the command flask run app.py



CI/CD
-----

-   After pushing the code to github the workflow will run the unit test case to check the working of app.
-   After merging the code the github workflow will create a custom AMI and push it into EC2 instance.
-   The artifact generated is stored in S3 bucket and deployed to an
    autoscaling group. ![ci-cd](https://user-images.githubusercontent.com/42703011/92802596-a7858700-f384-11ea-89db-85f0f8de8bc7.png)


Auto scaling groups
-------------------

-   Created auto scaling groups to scale the EC2 instances for the application to handle
    the webtraffic and keep the costs low when traffic is low
-   Created cloud watch alarms to scale up and scale down the EC2 instances

Serverless computing
--------------------

-   Created a pub/sub system with SNS and lambda function
-   When the user registers, a message is published to
    the SNS topic.
-   The lambda function checks for the entry of the email in DynamoDB if
    it has no entry then it inserts a record with a TTL of 5 minutes
    and sends the notification to the user with SES ![alt
    text]![lambda](https://user-images.githubusercontent.com/42703011/92802718-c126ce80-f384-11ea-843f-a06d1267bdd9.png)


[Packer](https://packer.io/)
----------------------------

-   Implemented CI to build out an AMI and share it between organization
    on AWS
-   Created provisioners and bootstrapped the RDS instance using shell script 
    
    
#Some Extra information

Building and deploying the flask app

flask run -p 3000


To check http status code
curl -v http://127.0.0.1:3000/healthz


To demo: 
mkdir newfolder
cd newfolder
git clone git@github.com:lareb-neu/webapp.git


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
