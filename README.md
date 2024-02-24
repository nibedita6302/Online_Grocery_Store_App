# Online Grocery Store App ~ Version 2

## About Project
Developed wireframe of a web-app for buying groceries online and updating of items sold by store managers. Used SQLite for database management and robust use of Flask and SQLAlchemy (Python) for backend for managing users, searching product, managing categories of product, selecting multiple items and admin management. Engineered a robust API using RESTful principles and login with authentication and authorization. User interface created using HTML, CSS, Bootstrap and Vue.js. Implemented Redis for caching. Currently working on Celery for asynchronous task processing, real-time event notifications and Webhooks for handling messaging queues.   

## Tech Stack
<img alt="Static Badge" src="https://img.shields.io/badge/Python-blue?style=plastic&logo=python&logoColor=yellow" height="25"> <img alt="Static Badge" src="https://img.shields.io/badge/SQLite_3-brightgreen?style=plastic&logo=sqlite&logoColor=white" height="25">
<img alt="Static Badge" src="https://img.shields.io/badge/SQLAlchemy-%23eb3a1f?style=plastic&logo=SQLAlchemy&logoColor=black" height="25">
<img alt="Static Badge" src="https://img.shields.io/badge/Flask-white?style=plastic&logo=flask&logoColor=black" height="25"> 
<img alt="Static Badge" src="https://img.shields.io/badge/Flask_Security_too-black?style=plastic&logo=flask&logoColor=white" height="25">
<img alt="Static Badge" src="https://img.shields.io/badge/Redis-%23ae1710?style=plastic&logo=redis&logoColor=white" height="25"> 
<img alt="Static Badge" src="https://img.shields.io/badge/Celery-brightgreen?style=plastic&logo=celery&logoColor=black" height="25">
<img alt="Static Badge" src="https://img.shields.io/badge/Messaging_Queues-orange?style=plastic&logo=stackexchange&logoColor=white" height="25">
<img alt="Static Badge" src="https://img.shields.io/badge/Git-%23ae1710?style=plastic&logo=git&logoColor=white" height="25">
<img alt="Static Badge" src="https://img.shields.io/badge/NPM-magenta?style=plastic&logo=npm&logoColor=white" height="25">
<img alt="Static Badge" src="https://img.shields.io/badge/Javascript-yellow?style=plastic&logo=Javascript&logoColor=black" height="25">
<img alt="Static Badge" src="https://img.shields.io/badge/VueJS-grey?style=plastic&logo=vue.js&logoColor=green" height="25">
<img alt="Static Badge" src="https://img.shields.io/badge/REST_API-%23f4f8af?style=plastic&logo=academia&logoColor=purple" height="25">
<img alt="Static Badge" src="https://img.shields.io/badge/Postman-white?style=plastic&logo=postman&logoColor=red" height="25">
<img alt="Static Badge" src="https://img.shields.io/badge/Linux-purple?style=plastic&logo=linux&logoColor=black" height="25">

## README 

Open Linux terminal. Make sure to have __python3__, __pip3__, __SQLite2__ and __Redis Server__ installed. Follow the following command to 
start the Online Grocery Store application.

### ------ TERMINAL 1 ------
```
$ bash local_setup.sh  ## creates environment and installs requirements 
$ bash local_run.sh		## runs main.py
```
Alternatively,
```
$ . .myenv/bin/activate
$ cd Flask-Backend/
$ python3 main.py
```
### ------ TERMINAL 2 ------
``` 
$ redis-server  # start redis server
```

### ------ TERMINAL 3 ------
``` 
$ bash local_workers.sh  # start celery worker
```
Alternatively,
```
$ . .myenv/bin/activate
$ cd Flask-Backend/
$ celery -A main.celery worker -l info
```

### ------ TERMINAL 4 ------
``` 
$ bash local_beat.sh  # start celery worker
```
Alternatively,
```
$ . .myenv/bin/activate
$ cd Flask-Backend/
$ celery -A main.celery beat -l info
```

### ------ TERMINAL 5 ------
```
$ cd frontend/
$ npm run serve  # start vue.js server
```

#### Go to browser and search for url: 
*http://localhost:8000/* for Home page and explore!

There is only One Admin allowed in the application with following credentials
#### Admin Login Credentials:
- Fork Repository
- Go to `Flask-Backend/application/data/default_data.py` *(Help: Check code line number 14 and 16)*
- Change `# put your email here` with your own email and `# put your password here` with your password
- Go to `Flask-Backend/application/jobs/setupEmail.py` *(Help: Check code line number 11-12)*
- Change `Your Email goes here` with your own email and `Replace with your Gmail App Password` with your Gmail App Password. 
    
Note:- For registering Store Managers, apply for approval through login page then, login as Admin 
to accept the Store Manager's approval. Now you can successfully login as a Store Manager!
