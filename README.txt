README 

Open Linux terminal. Make sure to have python3 and pip installed. Follow the following command to 
start the Online Grocery Store application.

------ TERMINAL 1 ------
$ bash local_setup.sh  ## creates environment and installs requirements 
$ bash local_run.sh		## runs main.py

Alternatively,
$ . .myenv/bin/activate
$ cd Flask-Backend/
$ python3 main.py

------ TERMINAL 2 ------
$ redis-server  # start redis server

------ TERMINAL 3 ------
$ bash local_workers.sh  # start celery worker

Alternatively,
$ . .myenv/bin/activate
$ cd Flask-Backend/
$ celery -A main.celery worker -l info

------ TERMINAL 4 ------
$ cd frontend/
$ npm run serve  # start vue.js server

Go to browser and search for url: 
http://localhost:8000/ for Home page and explore!

Admin Login Credentials:
Email: admin.12@grocery.com
Password: admin.12

Note:- For registering Store Managers, apply for approval through login page then, login as Admin 
to accept the Store Manager's approval. Now you can successfully login as a Store Manager!


