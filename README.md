# HumanActivityPredictionUsingSmartDevices
# Introduction 
TODO: Front End Web Application

## Getting Started

1. First we need to pull the docker image of DB. For that, we use the command:

docker pull dockercibin/hapd_mysql_image:latest
sudo docker run -d -p 3310:3306 --name my-mysql-container dockercibin/hapd_mysql_image

2. Next, we need to run the docker image in our local:
sudo docker run --name hasd_api  --network=host -p 7000:7000 -it dockercibin/hasd_api_image:latest

Next, coming to the front end application to go live:

First we need to install the libraries mentioned in requirements.txt

We have 3 screens in UI:

Home page
Select Time stamp - Activity page
Select Time range - Activity page

The app initialization starts from app.py file. This file is ran to up the application.
We use 'python app.py' command to run the application.

The blueprints of all the screens are registered in app.py.

Once the app is up, the development server will be hosted in the URL: http://127.0.0.1:5000


