""""
  ***   DOCUMENTATION *** 

"""


#   Welcome to Holagraph collaborative Software Backend with Django, Django REST Framework and Django Channels #

# To SetUp on Your Local Machine #

step 0: Python must be installed on local machine

step 1: pip install requirements.txt

step 2: python manage.py makemigrations

step 3: python manage.py migrate

step 4: python manage.py createsuperuser

step 5: python manage.py test 

# TODO - Only 1 Automated test Implemeted out of 3
# TODO - Automated Test for Django  - mark done
# TODO - Automated Test for Django REST Framework  - mark undone
# TODO - Automated Test for Django Channels  - mark undone

step 5: Go to http://127.0.0.1:8000/admin/    --- Login to admin interface

step 6: Go to http://127.0.0.1:8000/swagger/   --- To see automated documentation

step 7: Note group message in channel is real time and it was implemented with django channels and websocket - 

        For reference to code, visit asgi.py, consumers.py and routing.py

