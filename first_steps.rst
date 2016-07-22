First Steps
===========

1) Get modules specified in 'requirements.txt'

2) Clone Scheduler repository
   + -> git clone https://github.com/sjaa/scheduler.git [optional directory name]
   + -> cd <scheduler directory name>

3) Generate 'secrets.py' files
   + ->  cd schedule
   + ->  cp secrets_example.py secrets.py
   + [edit "secrets.py"]
   + ->  cd ../sched_announce
   + ->  cp secrets_example.py secrets.py
   + [edit "secrets.py"]

4) Setup database
   + -> python manage.py migrate

5) Setup super user - add an account for access
   + -> python manage.py createsuperuser
   + Specifiy user name, email, password

6) Customize configuration (e.g., location)
   Edit sched_ev/config.py

7) load sample event type and groups
   + -> python manage.py loaddata sample.json

8) Start Django server
   + -> python manage.py runserver

9) Modify event types
   + In web browser:
     http://127.0.0.1:8001/admin
   + Log in
   + Click on 'Event types'
   + Change event types to match locations specified in 6)

10) Follow steps in 'tutorial.rst'

